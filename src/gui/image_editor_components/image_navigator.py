class ImageNavigator:
    """Gerencia a navegação entre múltiplas imagens."""
    def __init__(self, image_paths, current_index=0):
        self.image_paths = image_paths
        self.current_index = current_index

    def has_next(self) -> bool:
        return self.current_index < len(self.image_paths) - 1

    def has_prev(self) -> bool:
        return self.current_index > 0

    def next_image(self) -> int:
        """Retorna o índice da próxima imagem, se existir."""
        if self.has_next():
            self.current_index += 1
        return self.current_index

    def prev_image(self) -> int:
        """Retorna o índice da imagem anterior, se existir."""
        if self.has_prev():
            self.current_index -= 1
        return self.current_index

    def get_current_image(self) -> str:
        """Retorna o caminho da imagem atual."""
        return self.image_paths[self.current_index]

    def get_image_count(self) -> int:
        return len(self.image_paths)
