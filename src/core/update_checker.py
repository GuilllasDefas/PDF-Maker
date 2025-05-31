import requests
import threading
import webbrowser
import logging
from src.config.config import APP_VERSION

class UpdateChecker:
    def __init__(self):
        self.github_repo = "GuilllasDefas/PDF-Maker"
        self.current_version = APP_VERSION
        
    def check_for_updates_async(self, callback):
        """Verifica atualizações de forma assíncrona."""
        def check():
            try:
                has_update, latest_version, download_url = self._check_github_prereleases()
                logging.debug(f"Verificação de updates: has_update={has_update}, latest_version={latest_version}")
                callback(has_update, latest_version, download_url)
            except Exception as e:
                logging.error(f"Erro ao verificar atualizações: {str(e)}")
                callback(False, None, None)
        
        threading.Thread(target=check, daemon=True).start()
    
    def _check_github_releases(self):
        """Verifica releases no GitHub."""
        url = f"https://api.github.com/repos/{self.github_repo}/releases/latest"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        
        release_data = response.json()
        latest_version = release_data['tag_name'].lstrip('v')
        
        # Encontrar o asset do setup
        download_url = release_data['html_url']
        for asset in release_data.get('assets', []):
            if 'Setup' in asset['name'] and asset['name'].endswith('.exe'):
                download_url = asset['browser_download_url']
                break
        
        has_update = self._is_newer_version(latest_version, self.current_version)
        return has_update, latest_version, download_url
    
    def _check_github_prereleases(self):
        """Verifica pre-releases no GitHub."""
        url = f"https://api.github.com/repos/{self.github_repo}/releases"
        logging.debug(f"Consultando API do GitHub: {url}")
        
        # Adiciona um User-Agent para evitar bloqueios da API
        headers = {"User-Agent": "PDF-Maker-Update-Checker"}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        releases = response.json()
        logging.debug(f"Total de releases encontradas: {len(releases)}")
        
        # Primeiro, tenta encontrar qualquer release, incluindo prereleases
        if not releases:
            logging.debug("Nenhuma release encontrada")
            return False, None, None
            
        # Verifica todas as releases, incluindo as que não são explicitamente marcadas como prerelease
        for release in releases:
            logging.debug(f"Analisando release: {release.get('tag_name')}, prerelease: {release.get('prerelease')}")
            
            latest_version = release['tag_name'].lstrip('v')
            download_url = release['html_url']
            
            # Encontrar o asset do setup
            for asset in release.get('assets', []):
                if 'Setup' in asset['name'] and asset['name'].endswith('.exe'):
                    download_url = asset['browser_download_url']
                    logging.debug(f"Encontrado asset de setup: {asset['name']}")
                    break
            
            has_update = self._is_newer_version(latest_version, self.current_version)
            logging.debug(f"Comparação de versão: {latest_version} > {self.current_version} = {has_update}")
            
            if has_update:
                return True, latest_version, download_url
        
        return False, None, None

    def _is_newer_version(self, latest, current):
        """Compara versões no formato x.y.z"""
        try:
            # Remove qualquer prefixo não-numérico (como "v")
            latest = latest.lstrip("v")
            current = current.lstrip("v")
            
            # Separa a versão principal de qualquer sufixo (como "-beta")
            latest_main = latest.split('-')[0]
            current_main = current.split('-')[0]
            
            latest_parts = [int(x) for x in latest_main.split('.')]
            current_parts = [int(x) for x in current_main.split('.')]
            
            max_len = max(len(latest_parts), len(current_parts))
            latest_parts.extend([0] * (max_len - len(latest_parts)))
            current_parts.extend([0] * (max_len - len(current_parts)))
            
            # Se versões principais são iguais, verifica sufixos
            if latest_parts == current_parts:
                # Se latest tem sufixo e current não, current é mais recente
                if '-' in latest and '-' not in current:
                    return False
                # Se current tem sufixo e latest não, latest é mais recente
                if '-' not in latest and '-' in current:
                    return True
                # Se ambos têm sufixos, faz comparação lexicográfica simples
                # Isso é aproximado, mas suficiente para a maioria dos casos
                if '-' in latest and '-' in current:
                    return latest.split('-')[1] > current.split('-')[1]
            
            return latest_parts > current_parts
        except Exception as e:
            logging.error(f"Erro ao comparar versões {latest} e {current}: {str(e)}")
            return False
    
    def open_download_page(self, url):
        """Abre a página de download no navegador."""
        webbrowser.open(url)
