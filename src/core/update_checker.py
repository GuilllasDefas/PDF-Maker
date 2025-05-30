import requests
import threading
import webbrowser
from src.config.config import APP_VERSION

class UpdateChecker:
    def __init__(self):
        self.github_repo = "GuilllasDefas/PDF_Maker"
        self.current_version = APP_VERSION
        
    def check_for_updates_async(self, callback):
        """Verifica atualizações de forma assíncrona."""
        def check():
            try:
                has_update, latest_version, download_url = self._check_github_releases()
                callback(has_update, latest_version, download_url)
            except:
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
    
    def _is_newer_version(self, latest, current):
        """Compara versões no formato x.y.z"""
        try:
            latest_parts = [int(x) for x in latest.split('.')]
            current_parts = [int(x) for x in current.split('.')]
            
            max_len = max(len(latest_parts), len(current_parts))
            latest_parts.extend([0] * (max_len - len(latest_parts)))
            current_parts.extend([0] * (max_len - len(current_parts)))
            
            return latest_parts > current_parts
        except:
            return False
    
    def open_download_page(self, url):
        """Abre a página de download no navegador."""
        webbrowser.open(url)
