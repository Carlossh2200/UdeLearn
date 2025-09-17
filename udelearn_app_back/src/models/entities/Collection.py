class Collection():

    def __init__(self,id=None,title=None,description=None,document=None) -> None:
        self.id = id
        self.title= title
        self.description = description
        self.document = document

    def to_JSON(self):
        return{
            'id':self.id,
            'title':self.title,
            'description':self.description,
            'document':self.document,
        }
    