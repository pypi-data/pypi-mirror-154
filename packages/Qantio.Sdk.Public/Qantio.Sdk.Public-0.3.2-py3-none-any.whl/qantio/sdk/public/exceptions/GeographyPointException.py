class GeographyPointException(Exception):
    
    def __init__(self, name:str, value:float, range:str):
        self.coodinate_name = name
        self.coodinate_value = value
        self.message = f"The {self.coodinate_name} value {self.coodinate_value} is not valid because {self.coodinate_name} is not in {range} range."
        super().__init__(self.message)

    def __str__(self) -> str:
        return f'{self.coodinate_name} : {self.coodinate_value} -> {self.message}'