# Les librairies 
#kivymd (kivy material design) pour le front de l'apk
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.button import MDRectangleFlatButton, MDFlatButton
from kivymd.uix.list import TwoLineAvatarIconListItem, ILeftBodyTouch
from kivymd.uix.selectioncontrol import MDCheckbox
from datetime import datetime

# IMPORTATION DE LA BDD
from database import Database
# INSTANCIATION DE LA CLASS BDD
db = Database()


class DialogContent(MDBoxLayout):
    """OUVRIE LA BOITE DE DIALOGUE DES TACHES"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ids.date_text.text = str(datetime.now().strftime('%A %d %B %Y'))

    
    def show_date_picker(self):
        """Ouverture du datepicker pour selectionner la date"""
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_save)
        date_dialog.open()

    def on_save(self, instance, value, date_range):
        date = value.strftime('%A %d %B %Y')
        self.ids.date_text.text = str(date)

# Apres la creation de la bd (les listes d'affichages)
class ListItemWithCheckbox(TwoLineAvatarIconListItem):
    ''''''

    def __init__(self, pk=None, **kwargs):
        super().__init__(**kwargs)
        # constructeur de la clé primaire
        self.pk = pk

    def mark(self, check, the_list_item):
        '''marqué la tache complete ou incomplete'''
        if check.active == True:
            the_list_item.text = '[s]'+the_list_item.text+'[/s]'
            db.mark_task_as_complete(the_list_item.pk)# ici pk
        else:
            the_list_item.text = str(db.mark_task_as_incomplete(the_list_item.pk))# ici pk

    def delete_item(self, the_list_item):
        '''Supprimer la tache'''
        self.parent.remove_widget(the_list_item)
        db.delete_task(the_list_item.pk)# ic pk

class LeftCheckbox(ILeftBodyTouch, MDCheckbox):
    '''Checkbox'''

# CLASSE PRINCIPALE DE L'APP
class MainApp(MDApp):
    task_list_dialog = None
    def build(self):
        # Confugurer la couleur 
        self.theme_cls.primary_palette = "Orange"
        self.title="Groupe 6"
        
    # Ouvrir la boite de dialogue pour ajouter une tache 
    def show_task_dialog(self):
        if not self.task_list_dialog:
            self.task_list_dialog = MDDialog(
                title="Creer une Tache",
                type="custom",
                content_cls=DialogContent(),
            )

        self.task_list_dialog.open()

    
    def show_data(self):
    
        self.dialog = MDDialog(title='Vos taches du jours',
                               text= str(db.get_tasks_today()), size_hint=(0.8, 1),
                               buttons=[MDFlatButton(text='Fermer', on_release=self.close_dialog_btn),
                                        MDFlatButton(text='More')]
                               )
        self.dialog.open()

    
    def close_dialog_btn(self, *args):
        self.dialog.dismiss()


    def on_start(self):
        # Recuperé les taches et les afficher lors du demarrage de l'app
        try:
            tache_complete, tache_incomplete = db.get_tasks()

            if tache_incomplete != []:
                for task in tache_incomplete:
                    add_task = ListItemWithCheckbox(pk=task[0],text=task[1], secondary_text=task[2])
                    self.root.ids.container.add_widget(add_task)

            if tache_complete != []:
                for task in tache_complete:
                    add_task = ListItemWithCheckbox(pk=task[0],text='[s]'+task[1]+'[/s]', secondary_text=task[2])
                    add_task.ids.check.active = True
                    self.root.ids.container.add_widget(add_task)
        except Exception as e:
            print(e)
            pass

    def close_dialog(self, *args):
        self.task_list_dialog.dismiss()

    def add_task(self, task, date_tache):
        '''Ajouter une tache a la liste des taches'''
        # print(task.text, date_tache)
        created_task = db.create_task(task.text, date_tache)

        # recuperé les details d'une tache
        self.root.ids['container'].add_widget(ListItemWithCheckbox(pk=created_task[0], text='[b]'+created_task[1]+'[/b]', secondary_text=created_task[2]))
        task.text = ''

if __name__ == '__main__':
    app = MainApp()
    app.run()
