class AnnotationElement:
    """Representa um elemento de anotação na imagem."""
    def __init__(self, element_type, properties, item_id):
        self.type = element_type  # 'text', 'arrow', 'rect', 'line'
        self.properties = properties  # coordenadas, cor, texto, etc.
        self.item_id = item_id  # ID do item no canvas
    
    def to_dict(self):
        """Converte o elemento para um dicionário para serialização."""
        return {
            'type': self.type,
            'properties': self.properties
        }
    
    @classmethod
    def from_dict(cls, data, item_id=None):
        """Cria um elemento a partir de um dicionário."""
        return cls(data['type'], data['properties'], item_id)