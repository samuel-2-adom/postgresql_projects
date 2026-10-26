from .database import init_db,drop_table,add_contact,delete_contact,update_contact
from .database import get_contacts,display,favorite,unfavorite,filter,stats

class ContactBook:

    def __init__(self,db=init_db()):
        self.db = db

    def drop_t(self):
        drop_table()

    def add_cont(self,f_name,l_name,phone,email,note=None):
        add_contact(f_name,l_name,phone,email,note=None)

    def delete_cont(self,contact_id):
        delete_contact(contact_id)

    def update_cont(self,contact_id,f_name,l_name,phone,email,note):
        update_contact(contact_id,f_name,l_name,phone,email,note)

    def get_cont(self):
        get_contacts()

    def displ(self):
        return display()

    def fav(self,contact_id):
        favorite(contact_id)

    def unfav(self,contact_id):
        unfavorite(contact_id)

    def filt(self,id=None,name=None,phone=None,email=None,favorite=False):
        filter(id,name,phone,email,favorite)

    def stat(self):
        stats()

if __name__ == "__main__":
    c_book = ContactBook()
    c_book.stat()
    if c_book.displ():
        pass
