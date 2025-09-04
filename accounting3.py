import tkinter as tkinter
from tkinter import Label,LabelFrame,Entry,Frame,Button,Canvas,BooleanVar,END,Tk,Widget,messagebox,Toplevel
from winsound import MessageBeep, MB_OK
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib import font_manager, rcParams
from tkinter import ttk as ttk
from PIL import Image, ImageTk
import requests
from dotenv import load_dotenv
from os import getenv,path
from threading import Thread
from time import time, perf_counter
import json
from ctypes import windll
from datetime import datetime, date, timedelta
import sqlite3 as sql
import random 
import numpy as np
start = perf_counter()

load_dotenv()
BACKEND_URL = getenv('BACKEND_URL')

light_dark= "#526D82"
mid_dark = "#3C5267"
sub_lightdark = "#27374D"

main_color = "#DAECF3"
sub_maincolor = "#85DADD"

text_color = "#DDE6ED"
sub_textcolor = "#8EA0AC"

error_color = '#EF4444'
success_color = '#28a745'

matplotlib_font = font_manager.FontProperties(fname='assets/monogram.ttf')
font_manager.fontManager.addfont('assets/monogram.ttf')
rcParams['font.family'] = 'monogram'
rcParams['font.size'] = 18
rcParams['text.color'] = text_color
rcParams['xtick.color'] = text_color
rcParams['ytick.color'] = text_color
rcParams['font.weight'] = 'bold'


window = Tk()
window.title('Budgit')
window.geometry('1400x720')
window.configure(background=light_dark)
remember_var = BooleanVar()

style = ttk.Style()
style.theme_use("default")
style.configure(
    "Custom.TCheckbutton",
    background=sub_lightdark,
    foreground=text_color,
    font=('monogram', 20),
    anchor = 'w'
)
style.map(
    "Custom.TCheckbutton",
    background=[
        ('active', sub_lightdark),
        ('selected', sub_lightdark),
        ('!active', sub_lightdark),
        ('!selected', sub_lightdark),
        ('pressed', sub_lightdark),
        ('focus', sub_lightdark)
    ]
)
style.map(
    'TCombobox',
    fieldbackground=[('readonly',light_dark),('disabled',light_dark)],
    arrowcolor = [('readonly',sub_lightdark),('disabled',sub_lightdark)]
)

style.configure('Treeview',background = light_dark, foreground=main_color,font=('monogram',20,'bold'), fieldbackground=light_dark,borderwidth=0,row_height=25)
style.configure('Treeview.Heading',background = sub_lightdark, foreground=main_color,font=('monogram',20))
style.configure('TScrollbar',background = sub_lightdark, foreground= light_dark,arrowcolor=light_dark,troughcolor=light_dark)
style.configure('TCombobox',background = mid_dark, fieldbackground = [('readonly', light_dark),('disabled',light_dark)],foreground=text_color,font=('monogram',20),arrowcolor=sub_lightdark)
window.option_add('*TCombobox*Listbox.background', mid_dark)
window.option_add('*TCombobox*Listbox.font', ('monogram',20))
window.option_add('*TCombobox*Listbox.foreground', text_color)
window.option_add('*TCombobox*Listbox.selectBackground', sub_lightdark)

bootoption_page = Frame(window,background=light_dark)
signup_page = Frame(window, background=light_dark)
signup_initialise_page = Frame(window, background=light_dark)
login_page = Frame(window,background=light_dark)
accounting_page = Frame(window, background=light_dark)
loading_page = Frame(window, background=light_dark)
tab_list = [login_page,signup_page,accounting_page,bootoption_page,loading_page,signup_initialise_page]

#Font loading
font_path = path.abspath("assets/monogram.ttf")
windll.gdi32.AddFontResourceW(font_path)

custom_font = 'monogram'

page_built = {
    'bootoption_page' : False,
    'signup_page' : False,
    'signup_initialise_page' : False,
    'login_page' : False,
    'accounting_page' : False,
}

page_linked = {
    'bootoption_page' : ['login_page'],
    'signup_page' : ['login_page'],
    'signup_initialise_page' : [],
    'login_page' : ['signup_page'],
    'accounting_page' : [],
}

account_formula = {
    'assets':{
        'assets' : [False,True],
        'expenses' : [False,True],
        'liabilities' : [False,False],
        'equity' : [False,False],
        'access_list' : ['assets','expenses','liabilities','equity']

    },
    'liabilities' : {
        'assets' : [True,True],
        'liabilities' : [False,True],
        'expenses' : [False,True],
        'equity':[False,False],
        'access_list' : ['assets','expenses','liabilities','equity']
    },
    'equity' : {
        'assets' : [True,True],
        'liability' : [True,True],
        'expenses' : [False,True],
        'access_list' : ['assets','expenses','liabilities']
    },
    'revenue' : {
        'assets' : [True,True],
        'equity' : [True,True],
        'access_list' : ['assets','equity']
    }
}


logo_image = Image.open('image/logo.png').resize((32,32), Image.LANCZOS)
logo_photo = ImageTk.PhotoImage(logo_image)
window.iconphoto(True, logo_photo)

logo_google_image = Image.open('image/google_logo.png').resize((32,32), Image.LANCZOS)
logo_google_photo = ImageTk.PhotoImage(logo_google_image)

logo_github_image = Image.open('image/github_logo.png').resize((32,32), Image.LANCZOS)
logo_github_photo = ImageTk.PhotoImage(logo_github_image)

dashboard_image = Image.open('image/dashboard.png').resize((14,14), Image.LANCZOS)
dashboard_photo = ImageTk.PhotoImage(dashboard_image)

transaction_image = Image.open('image/transaction.png').resize((14,14), Image.LANCZOS)
transaction_photo = ImageTk.PhotoImage(transaction_image)

budget_image = Image.open('image/budget.png').resize((14,14), Image.LANCZOS)
budget_photo = ImageTk.PhotoImage(budget_image)

wallet_image = Image.open('image/wallet.png').resize((14,14), Image.LANCZOS)
wallet_photo = ImageTk.PhotoImage(wallet_image)

chatgpt_image = Image.open('image/chatgpt.png').resize((14,14), Image.LANCZOS)
chatgpt_photo = ImageTk.PhotoImage(chatgpt_image)

setting_image = Image.open('image/setting.png').resize((14,14), Image.LANCZOS)
setting_photo = ImageTk.PhotoImage(setting_image)

class API:
    def __init__(self):
        self.key = None

    def convert_List_format(self, lists=list,changed_format=list): # basicall [1,2,3,4] change to [2,4,1,2]
        
        list_size = len(lists)

        if len(changed_format) > len(lists):
            return False

        new_list = []

        for i in changed_format:
            if i > (list_size-1):
                return False
            new_list.append(lists[i])

        return new_list

    def online_login_email(self, email_widget,password_widget,error_msg_widget,remember_me_var):
        if email_widget and password_widget :
            email = email_widget.get()
            password = password_widget.get()
        else:
            return 'all the widget dont exist'
        
        if email == 'Email' or password == 'Password':
            error_msg_widget.config(text=''),
            error_msg_widget.config(text='Please enter your username and password', fg = error_color)
            return

        Thread(target=self.online_login_email_thread,args=(email,password,error_msg_widget,remember_me_var)).start()
    def online_login_email_thread(self,email,password,error_msg_widget,remember_me_var):
        try:
            response = requests.post(url=f'{BACKEND_URL}/online_login_email',json=({'email':email,'password':password}),timeout=10)
            if response.status_code == 200:
                self.key = response.json().get('token')
                if remember_me_var:
                    with open('config.json', 'w+') as file:
                        payload = {
                            'email': email,
                            'password': password
                        }
                        json.dump(payload, file)
                window.after(0,lambda: load_page('accounting_page'))
                return
            else:
                error = response.json().get('error')
                window.after(0, lambda: error_msg_widget.config(text=''))
                window.after(0, lambda: error_msg_widget.config(text=error, fg = error_color))
                return

        except requests.exceptions.ConnectionError:
            window.after(0, lambda: error_msg_widget.config(text=''))
            window.after(0, lambda: error_msg_widget.config(text='Connection to Server Failed', fg = error_color) )
            return

        except Exception as e:
            error_msg = str(e)
            window.after(0, lambda: error_msg_widget.config(text=''))
            window.after(0, lambda: error_msg_widget.config(text=error_msg, fg = error_color) )
            return

    def online_signup_email(self, email_widget,password_widget,confirm_password_widget,error_msg_widget):
        if email_widget and password_widget:
            email = email_widget.get()
            password = password_widget.get()
            confirm_password = confirm_password_widget.get()
        else:
            return 'all the widget dont exist'
        
        if email == 'Email' or password == 'Password':
            error_msg_widget.config(text='')
            error_msg_widget.configure(text='Please enter your username and password', fg = error_color)
            return
        
        if password != confirm_password:
            error_msg_widget.config(text='')
            error_msg_widget.configure(text='Confirm password doesnt match.', fg = error_color)
            return
        
        Thread(target=self.online_signup_email_thread,args=(email,password,error_msg_widget)).start()
    def online_signup_email_thread(self,email,password,error_msg_widget):
        try:
            check_response = requests.post(
                url= f'{BACKEND_URL}/check_user_exists',
                json={'email':email}
            )

            if check_response.status_code == 200:
                if check_response.json().get('exists') == True:
                    window.after(0, lambda: error_msg_widget.config(text=''))
                    window.after(0, lambda: error_msg_widget.configure(text='An account with this email already exists', fg = error_color) )
                    return
                
            else:
                error_msg = check_response.json().get('error')
                window.after(0, lambda: error_msg_widget.config(text=''))
                window.after(0, lambda: error_msg_widget.configure(text=error_msg, fg = error_color) )
                return
            

            response = requests.post(
                url=f'{BACKEND_URL}/online_signup_email',
                json={'email':email,'password':password}
                )
            
            if response.status_code == 200:
                window.after(0, lambda: error_msg_widget.config(text=''))
                window.after(0,error_msg_widget.configure(text = 'Please check your email to confirm', fg = success_color))
            else:
                error_msg = response.json().get('error')
                window.after(0,error_msg_widget.configure(text = error_msg))

        except requests.exceptions.ConnectionError:
            window.after(0, lambda: error_msg_widget.config(text=''))
            window.after(0, lambda: error_msg_widget.config(text='Connection to Server Failed', fg = error_color) )
            return

        except Exception as e:
            error_msg = str(e)
            window.after(0, lambda: error_msg_widget.configure(text=error_msg, fg = error_color) )
            return
        
    def offline_fetch_account(self):
        connect = sql.connect('database.db')
        cursor = connect.cursor()
        cursor.execute('SELECT account_type FROM account_types')
        return cursor.fetchall()
    
    def offline_insert_category(self,lists):
        connect = sql.connect('database.db')
        cursor = connect.cursor()

        if len(lists) != 0:
            for i in lists:
                cursor.execute('INSERT INTO accounts(account,account_type) VALUES (?, ?)',i)
        else:
            return False
        
    def offline_confirm_setup(self,lists=list,changed_format=list,convert=bool):
        connect = sql.connect('database.db')
        cursor = connect.cursor()

        final_list = []

        if convert:
            for i in lists:
                added_list = self.convert_List_format(i,changed_format)
                final_list.append(added_list)
            cursor.executemany('INSERT INTO accounts(account, account_type) VALUES(?,?)',final_list)
            connect.commit()
        else:
            cursor.executemany('INSERT INTO accounts(account, account_type) VALUES(?,?)',lists)
            connect.commit()

    def fetch_today_entry(self,treeview,extra_func=False):
        today = date.today().strftime('%d-%m-%Y').split('-')
        try:
            connect = sql.connect('database.db')
            cursor = connect.cursor()
            cursor.execute('SELECT * FROM transactions WHERE day = ? AND month = ? AND year=?',today)

            for index,value in enumerate(cursor.fetchall()):
                treeview.insert('','end',values=[index+1] + list(value))
            if extra_func:
                extra_func(True)

        except:
            pass

    def offline_add_entry(self,from_type_widget,from_account_widget,to_type_widget,to_account_widget,error_msg_widget,date_widget,amount_widget,description_widget):
        from_type = from_type_widget.get()
        from_account = from_account_widget.get()
        to_type = to_type_widget.get()
        to_account = to_account_widget.get()
        date = date_widget
        amount = amount_widget.get()
        description = description_widget.get()

        if not all([from_type, from_account, to_type, to_account, date, amount, description]) or date == '---':
            error_msg_widget.configure(text='Please fill in all fields')
            window.after(3000,lambda:error_msg_widget.configure(fg=error_color,text=''))
            return False, []

        try:
            amount = float(amount)
            if len(str(int(amount))) > 17:
                error_msg_widget.configure(text='Amount is Too big!')
                window.after(3000,lambda:error_msg_widget.configure(fg=error_color,text=''))
                return False, []
        except Exception:
            error_msg_widget.configure(text='Make sure amount is an Number')
            window.after(3000,lambda:error_msg_widget.configure(fg=error_color,text=''))
            return False, []
        
        if amount <= 0:
            error_msg_widget.configure(text='Please input an ammount more than 0')
            window.after(3000,lambda:error_msg_widget.configure(fg=error_color,text=''))
            return False, []

        if len(description) > 50:
            error_msg_widget.configure(text='Description is too long (max 50 characters)')
            window.after(3000,lambda:error_msg_widget.configure(fg=error_color,text=''))
            return False, []
        try:
            date = datetime.strptime(date,'%d-%m-%Y')
            date = datetime.strftime(date,'%d-%m-%Y')
        except Exception as e:
            error_msg_widget.configure(text='Invalid Date make sure its DD-MM-YY format and be in calendar')
            window.after(3000,lambda:error_msg_widget.configure(fg=error_color,text=''))
            return False, []


        date_list = date.split('-')

        connect = sql.connect('database.db')
        cursor = connect.cursor()
        cursor.execute('PRAGMA foreign_keys = ON;')

        cursor.execute('INSERT INTO transactions (from_account_type, from_account, to_account_type, to_account, day, month, year, description, amount) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', (from_type, from_account,to_type,to_account,date_list[0],date_list[1],date_list[2],description,amount))

        error_msg_widget.configure(fg=success_color,text='Sucessfully Added a log in Transactions')
        window.after(3000,lambda:error_msg_widget.configure(fg=error_color,text=''))
        cursor.execute('SELECT id FROM transactions WHERE id = last_insert_rowid()')
        ids = cursor.fetchall()[0][0]
        connect.commit()
        connect.close()
        return True, [ids,from_type,from_account,to_type,to_account,date,description,amount]

    def offline_remove_entry(self,ids=int,error_msg_widget=Label):
        connect = sql.connect('database.db')
        cursor = connect.cursor()
        cursor.execute('PRAGMA foreign_keys = ON;')

        #delete part very careful
        cursor.execute('DELETE FROM transactions WHERE id = ?',(ids,))

        error_msg_widget.configure(fg=success_color,text='Sucessfully removed a log in Transactions')
        window.after(3000,lambda:error_msg_widget.configure(fg=error_color,text=''))
        connect.commit()
        connect.close()
        return True

    def offline_edit_entry(self,ids,from_type_widget,from_account_widget,to_type_widget,to_account_widget,error_msg_widget,date_widget,amount_widget,description_widget,search_return_list=False):
        from_type = from_type_widget.get()
        from_account = from_account_widget.get()
        to_type = to_type_widget.get()
        to_account = to_account_widget.get()
        date= date_widget
        amount = amount_widget.get()
        description = description_widget.get()

        if not from_type or not from_account or not to_type or not to_account or not date or not amount or not description:
            error_msg_widget.configure(text='Please Fill in All the Fields')
            window.after(3000,lambda:error_msg_widget.configure(fg=error_color,text=''))
            return False,[]

        try:
            amount = float(amount)
            if len(str(int(amount))) > 17:
                error_msg_widget.configure(text='Amount is Too big!')
                window.after(3000,lambda:error_msg_widget.configure(fg=error_color,text=''))
                return False, []
        except Exception:
            error_msg_widget.configure(text='Make sure amount is an Number')
            window.after(3000,lambda:error_msg_widget.configure(fg=error_color,text=''))
            return False, []

        if len(description) > 50:
            error_msg_widget.configure(text='Description is too long (max 50 characters)')
            window.after(3000,lambda:error_msg_widget.configure(fg=error_color,text=''))
            return False, []

        try:
            date = datetime.strptime(date,'%d-%m-%Y')
            date = datetime.strftime(date,'%d-%m-%Y')
        except Exception as e:
            error_msg_widget.configure(text='Invalid Date make sure its DD-MM-YY format and be in calendar')
            window.after(3000,lambda:error_msg_widget.configure(fg=error_color,text=''))
            return False,[]

        connect = sql.connect('database.db')
        cursor = connect.cursor()
        cursor.execute('PRAGMA foreign_keys = ON;')

        split_date = date.split('-')
        #Update the new transaction
        cursor.execute('UPDATE transactions SET from_account_type = ?, from_account = ?, to_account_type = ?, to_account = ?, day = ?, month = ?, year = ?, description = ?, amount = ? WHERE id = ?', (from_type,from_account,to_type,to_account,split_date[0],split_date[1],split_date[2],description,amount,ids))

        error_msg_widget.configure(fg=success_color,text='Sucessfully edited a log in Transactions')
        window.after(3000,lambda:error_msg_widget.configure(fg=error_color,text=''))

        connect.commit()
        connect.close()

        if search_return_list == True:
            return True,[ids,from_type,from_account,to_type,to_account,date,description,amount]
        else:
            return True,[]

    def offline_search_entry(self,from_type_widget,from_account_widget,to_type_widget,to_account_widget,error_msg_widget,date_widget,amount_widget,description_widget):
        from_type = from_type_widget.get()
        from_account = from_account_widget.get()
        to_type = to_type_widget.get()
        to_account = to_account_widget.get()
        date= date_widget
        amount = amount_widget.get()
        description = description_widget.get()

        query = 'SELECT * FROM transactions WHERE 1=1'
        data = []
        
    def offline_fetch_account_from_type(self,param):
        connect = sql.connect('database.db')
        cursor = connect.cursor()
        cursor.execute('SELECT account FROM accounts WHERE account_type = ?', (str(param),))
        placed_value = [row[0] for row in cursor.fetchall()]
        connect.close()
        return placed_value

    def offline_fetch_accounts(self):
        connect = sql.connect('database.db')
        cursor = connect.cursor()
        cursor.execute('SELECT id,account_type,account,transaction_count,actual_value FROM accounts ')
        temp = cursor.fetchall()
        connect.close()
        return temp

    def offline_add_account(self,type_widget,account_widget,error_msg_widget):
        types = type_widget.get()
        account = account_widget.get()

        if types == '' or account in ['\u200BEnter Here','']:
            error_msg_widget.configure(fg=error_color,text='Please fill in all the Entry Fields')
            window.after(3000,lambda:error_msg_widget.configure(fg=error_color,text=''))
            return False,[]
        
        if len(account) > 25:
            error_msg_widget.configure(fg=error_color,text='Account Name is too long! (max 25 characters)')
            window.after(3000,lambda:error_msg_widget.configure(fg=error_color,text=''))
            return False,[]
        
        connect = sql.connect('database.db')
        cursor = connect.cursor()
        cursor.execute('PRAGMA foreign_keys = ON')
        try:
            cursor.execute('INSERT INTO accounts (account,account_type) VALUES (?,?)', [account,types])
        except Exception as e:
            connect.close()
            error_msg_widget.configure(fg=error_color,text='Account Already Exists!')
            window.after(3000,lambda:error_msg_widget.configure(fg=error_color,text=''))
            return False, []
        
        ids = cursor.lastrowid
        connect.commit()
        connect.close()
        
        error_msg_widget.configure(fg=success_color,text='Succesfully Added a New Account')
        window.after(3000,lambda:error_msg_widget.configure(fg=error_color,text=''))
        return True, [ids,types,account,0,0]
        
    def offline_remove_account(self,ids,error_msg_widget,account_widget):
        account_widgets = account_widget.get()
        connect = sql.connect('database.db')
        cursor = connect.cursor()
        cursor.execute('PRAGMA foreign_keys = ON')

        try:
            cursor.execute('DELETE FROM accounts WHERE id = ?', [ids,])
        except Exception as e:
            connect.close()
            error_msg_widget.configure(fg=error_color,text=e)
            window.after(3000,lambda:error_msg_widget.configure(fg=error_color,text=''))
            return False
        
        connect.commit()
        connect.close()

        error_msg_widget.configure(fg=success_color,text=f'Succesfully Removed {account_widgets} from Account')
        window.after(3000,lambda:error_msg_widget.configure(fg=error_color,text=''))
        return True

    def offline_edit_account(self,type_widget,account_widget,error_msg_widget,ids):
        types = type_widget.get()
        account = account_widget.get()

        connect = sql.connect('database.db')
        cursor = connect.cursor()
        cursor.execute('PRAGMA foreign_keys = ON')

        try:
            cursor.execute('UPDATE accounts SET account = ?, transaction_count = 0, actual_value = 0 WHERE id = ?', [account, ids])
        except Exception as e:
            connect.close()
            error_msg_widget.configure(fg=error_color,text=f'{account} already existed in the list')
            window.after(3000,lambda:error_msg_widget.configure(fg=error_color,text=''))
            return False, []
        
        connect.commit()
        connect.close()

        error_msg_widget.configure(fg=success_color,text=f'Succesfully Edited {account} from Account')
        window.after(3000,lambda:error_msg_widget.configure(fg=error_color,text=''))
        return True, [types,account,0,0]

    def offline_search_account(self,type_widget,account_widget,error_msg_widget):
        types = type_widget.get()
        account = account_widget.get()

        data_list = []
        query = 'SELECT * FROM accounts WHERE 1=1'

        if types != '':
            query += ' AND account_type = ?'
            data_list.append(types)

        if account != '' and account != '\u200BEnter Here':
            query += ' AND account LIKE ?'
            data_list.append(account)

        connect = sql.connect('database.db')
        cursor = connect.cursor()
        try:
            cursor.execute(query,data_list)
            res = cursor.fetchall()
        except Exception as e:
            connect.close()
            error_msg_widget.configure(fg=error_color,text=e)
            window.after(3000,lambda:error_msg_widget.configure(fg=error_color,text=str(e)))
            return False, []
        
        connect.close()

        error_msg_widget.configure(fg=success_color,text=f'Succesfully Searched')
        window.after(3000,lambda:error_msg_widget.configure(fg=error_color,text=''))
        return True, res

    def offline_update_account(self,treeview,error_msg_widget):
        values = treeview.get_children()
        lists = [treeview.item(i, 'values')[1] for i in values]
        parentheses = ','.join(['?'] * len(lists))

        try:
            connect = sql.connect('database.db')
            cursor = connect.cursor()
            cursor.execute(f'SELECT * FROM accounts WHERE id IN ({parentheses})', lists)
            res_lists = cursor.fetchall()

        except Exception as e:
            connect.close()
            error_msg_widget.configure(fg=error_color,text=str(e))
            window.after(3000,lambda:error_msg_widget.configure(fg=error_color,text=''))
            return False, []
        
        return True, res_lists
    
    def offline_graph_plotting(self,start_date_widget,end_date_widget,account_type_widget,account_widget,graph_type_widget,error_msg_widget,graph_line_color_widget):
        start_date = start_date_widget
        end_date = end_date_widget
        account_type = account_type_widget.get()
        account = account_widget.get()
        graph_types = graph_type_widget.get()
        graph_line_color = graph_line_color_widget.get()
        

        #Date checking
        try:
            if start_date in ['\u200BDD-MM-YY',''] and  end_date in ['\u200BDD-MM-YY', '']:
                error_msg_widget.configure(fg=error_color,text='Please fill in the dates')
                window.after(3000,lambda:error_msg_widget.configure(fg=error_color,text=''))
                return False, [], '', ''
            
            start_date_list = start_date.split('-')
            end_date_list = end_date.split('-')

            if not len(start_date_list) == 3 or not len(end_date_list) == 3:
                error_msg_widget.configure(fg=error_color,text='Date is incomplete (eg.20-04-2025)')
                window.after(3000,lambda:error_msg_widget.configure(fg=error_color,text=''))
                return False, [], '', ''
            
            try:
                date1 = datetime.strptime(start_date,'%d-%m-%Y')
                date2 = datetime.strptime(end_date,'%d-%m-%Y')
            except Exception:
                error_msg_widget.configure(fg=error_color,text='Date is incomplete (eg.20-04-2025)')
                window.after(3000,lambda:error_msg_widget.configure(fg=error_color,text=''))
                return False, [], '', ''

            if date1 > date2:
                error_msg_widget.configure(fg=error_color,text='Start date is bigger than End date!')
                window.after(3000,lambda:error_msg_widget.configure(fg=error_color,text=''))
                return False, [], '', ''         
        except Exception as e:
            error_msg_widget.configure(fg=error_color,text='Invalid Date format (eg.20-04-2025)')
            window.after(3000,lambda:error_msg_widget.configure(fg=error_color,text=''))
            return False, [], '', ''
        
        if account_type == '\u200BEnter Here' or account_type == '' or graph_types == '' or graph_line_color == '':
            error_msg_widget.configure(fg=error_color,text='Please fill in all the fields')
            window.after(3000,lambda:error_msg_widget.configure(fg=error_color,text=''))
            return False, [], '', ''
        
        if graph_types in ['Amount', 'Total Amount']:graph_type='amount,'
        else: graph_type = 'transaction_count,'

        query = f"""
        SELECT {graph_type}day,month,year FROM daily_total
        WHERE
            (CAST(year AS TEXT) || '-' ||
            printf('%02d', month) || '-' ||
            printf('%02d', day)) BETWEEN ? AND ?
        """
        try:
            start_date_sql = datetime.strptime(start_date, "%d-%m-%Y").strftime("%Y-%m-%d")
            end_date_sql = datetime.strptime(end_date, "%d-%m-%Y").strftime("%Y-%m-%d")
            data = [start_date_sql,end_date_sql]
        except:
            error_msg_widget.configure(fg=error_color,text='Invalid Date format (eg.20-04-2025)')
            window.after(3000,lambda:error_msg_widget.configure(fg=error_color,text=''))
            return False, [], '', ''
        
        if graph_types == 'Total Amount':
            query2 = '''SELECT COALESCE(SUM(amount), 0) AS total FROM daily_total WHERE (CAST(year AS TEXT)|| '-' || printf('%02d', month) || '-' || printf('%02d', day)) < ? '''
            data2 = [start_date_sql]
        
        if account != '' and account_type != '':
            query += 'AND account = ?'
            data.append(account)
            if graph_types == 'Total Amount':
                query2 += 'AND account = ?'
                data2.append(account)

        if account_type:
            query += ' AND account_type = ?'
            data.append(account_type)
            if graph_types == 'Total Amount':
                query2 += 'AND account_type = ?'
                data2.append(account_type)

        query += '\nORDER BY year ASC, month ASC, day ASC'
        
        try:
            connect = sql.connect('database.db')
            cursor = connect.cursor()
            cursor.execute(query,data)
            data_list = cursor.fetchall()
            date1 = datetime.strptime(start_date, "%d-%m-%Y")
            date2 = datetime.strptime(end_date, "%d-%m-%Y")
            days_difference = abs((date2 - date1).days) + 1
            current_date = date1
            date_list = []

            while current_date <= date2:
                date_list.append(current_date)
                current_date += timedelta(days=1)

            res = [[0.0]*days_difference, date_list]
            if graph_types == 'Total Amount':
                cursor.execute(query2, data2)
                Amount_till_start_date = int(cursor.fetchone()[0])

            for i in data_list:
                i = list(i)
                date2 = datetime.strptime(f'{i[1]}-{i[2]}-{i[3]}', "%d-%m-%Y")
                days_difference = abs((date2 - date1).days)
                if graph_types == 'Total Amount':
                    Amount_till_start_date += i[0]
                    res[0][days_difference] = Amount_till_start_date
                else:
                    res[0][days_difference] += abs(i[0])

            last_value = 0
            if graph_types == 'Total Amount':
                for index,value in enumerate(res[0]):
                    if value != 0.0 :
                        last_value = value
                    else:
                        res[0][index] =  last_value

            connect.close()

        except Exception as e:
            error_msg_widget.configure(fg=error_color,text=str(e))
            window.after(3000,lambda:error_msg_widget.configure(fg=error_color,text=''))
            return False, [], '', ''
        error_msg_widget.configure(fg=success_color,text='Successfully Plot the Graph')
        window.after(3000,lambda:error_msg_widget.configure(fg=error_color,text=''))
        return True , res, graph_types,graph_line_color

    def offline_budget_add(self,account_type_widget,account_widget,duration_widget,budget_value_widget,error_msg_widget):
        account_type = account_type_widget.get()
        account = account_widget.get()
        duration = duration_widget.get()
        budget_value = budget_value_widget.get()

        if account_type == '' or account == '' or duration == '' or budget_value in ['\u200BEnter Here','']:
            error_msg_widget.configure(text='Please Fill in All Fields')
            window.after(3000, lambda:error_msg_widget.configure(text='', fg=error_color) )
            return False, []
        
        try:
            budget_value = float(budget_value)
            if len(str(int(budget_value))) > 17:
                error_msg_widget.configure(text='Budget goal is Too Large!')
                window.after(3000, lambda:error_msg_widget.configure(text='', fg=error_color) )
                return False, []

        except Exception:
            error_msg_widget.configure(text='Budget isnt filled with a number!')
            window.after(3000, lambda:error_msg_widget.configure(text='', fg=error_color) )
            return False, []

        
        
        if float(budget_value) <= 0 :
            error_msg_widget.configure(text='Budget value cant be less than 0')
            window.after(3000, lambda:error_msg_widget.configure(text='', fg=error_color) )
            return False, []
        
        try:
            connect = sql.connect('database.db')
            cursor = connect.cursor()

            cursor.execute('INSERT INTO budget(account_type,account,duration,budget_value) VALUES (?,?,?,?)', (account_type,account,duration,float(budget_value)))
            cursor.execute('SELECT * FROM budget WHERE account = ?', (account,))
            res = (cursor.lastrowid,account_type,account,duration,budget_value)
            connect.commit()
        except Exception as e:
            error_msg_widget.configure(text=str(e))
            window.after(3000, lambda:error_msg_widget.configure(text='', fg=error_color) )
            connect.close()
            return False, []
        connect.close()
        error_msg_widget.configure(text=f'Successfully Added a New Budget ! ({account_type}, {account})', fg=success_color)
        window.after(3000, lambda:error_msg_widget.configure(text='', fg=error_color) )
        return True, res

    def offline_budget_remove(self,account_type_widget,account_widget,duration_widget,budget_value_widget,error_msg_widget):
        account_type = account_type_widget.get()
        account = account_widget.get()
        duration = duration_widget.get()
        budget_value = budget_value_widget.get()

        if account_type == '' or account == '' or duration == '' or budget_value in ['\u200BEnter Here','']:
            error_msg_widget.configure(text='Please Fill in All Fields')
            window.after(3000, lambda:error_msg_widget.configure(text='', fg=error_color) )
            return False

        try:
            connect = sql.connect('database.db')
            cursor = connect.cursor()

            cursor.execute('DELETE FROM budget WHERE account = ?', (account,))
            connect.commit()

        except Exception as e:
            error_msg_widget.configure(text=str(e))
            window.after(3000, lambda:error_msg_widget.configure(text='', fg=error_color) )
            connect.close()
            return False
        error_msg_widget.configure(text=f'Successfully Removed ({account_type},{account})',fg=success_color)
        window.after(3000, lambda:error_msg_widget.configure(text='', fg=error_color) )
        return True

    def offline_budget_edit(self,account_type_widget,account_widget,duration_widget,budget_value_widget,error_msg_widget):
        account_type = account_type_widget.get()
        account = account_widget.get()
        duration = duration_widget.get()
        budget_value = budget_value_widget.get()

        if account == '' or duration == '' or budget_value in ['\u200BEnter Here','']:
            error_msg_widget.configure(text='Please Fill in All Fields')
            window.after(3000, lambda:error_msg_widget.configure(text='', fg=error_color) )
            return False, []

        try:
            budget_value = float(budget_value)
            if len(str(int(budget_value))) > 17:
                error_msg_widget.configure(text='Budget goal is Too Large!')
                window.after(3000, lambda:error_msg_widget.configure(text='', fg=error_color) )
                return False, []
        except Exception:
            error_msg_widget.configure(text='Budget Value isnt a Number!')
            window.after(3000, lambda:error_msg_widget.configure(text='', fg=error_color) )
            return False, []

        if budget_value < 1:
            error_msg_widget.configure(text='Budget Value cant be less than 0!')
            window.after(3000, lambda:error_msg_widget.configure(text='', fg=error_color) )
            return False, []

        try:
            connect = sql.connect('database.db')
            cursor = connect.cursor()

            cursor.execute('UPDATE budget SET duration = ?, budget_value = ? WHERE account = ? RETURNING *', (duration,budget_value,account,))
            res = list(cursor.fetchone())
            connect.commit()

        except Exception as e:
            error_msg_widget.configure(text=str(e))
            window.after(3000, lambda:error_msg_widget.configure(text='', fg=error_color) )
            connect.close()
            return False, []
        error_msg_widget.configure(text=f'Successfully Edited ({account_type},{account})',fg=success_color)
        window.after(3000, lambda:error_msg_widget.configure(text='', fg=error_color) )
        connect.close()
        return True, res

    def offline_budget_search(self,account_type_widget,account_widget,duration_widget,budget_value_widget,error_msg_widget):
        account_type = account_type_widget.get()
        account = account_widget.get()
        duration = duration_widget.get()
        budget_value = budget_value_widget.get()

        query = 'SELECT * FROM budget WHERE 1=1'
        data = []

        if account_type != '':
            query += ' AND account_type = ?'
            data.append(account_type)
        
        if account != '':
            query += ' AND account = ?'
            data.append(account)

        if duration != '':
            query += ' AND duration = ?'
            data.append(duration)

        if budget_value not in ['\u200BEnter Here','']:
            query += ' AND budget_value = ?'
            data.append(budget_value)

        try:
            connect = sql.connect('database.db')
            cursor = connect.cursor()

            cursor.execute(query,data)
            res = cursor.fetchall()
        except Exception as e:
            error_msg_widget.configure(text=str(e))
            window.after(3000, lambda:error_msg_widget.configure(text='', fg=error_color) )
            connect.close()
            return False, []
        
        error_msg_widget.configure(text='Successfully searched and results displayed',fg=success_color)
        window.after(3000, lambda:error_msg_widget.configure(text='', fg=error_color) )
        connect.close()
        return True, res

    def offline_budget_graph_calc(self,list_of_value,date=None):
        res = [[],[],[],[]] #Total
        res2 = []
        duration = ''
        calculate_dict = {
            'daily': [1, 7, 365/12, 365],
            'monthly': [1/30.44, 30.44/7, 1, 12/1],
            'yearly': [1/365, 52.143/1, 1/12, 1],
            'weekly': [1/7, 1, 4.345, 52.143]
            } 
        calculate_part = {
            'daily' : 0,
            'monthly' : 2,
            'yearly' : 3,
            'weekly' : 1,
        }
        try:
            if len(list_of_value) == 0 :
                return False, [], []
            query = 'SELECT SUM(amount) AS total_amount FROM daily_total WHERE 1=1'
            data = []

            if date[2] != '':
                query += ' AND year = ?'
                data.append(int(date[2]))
                duration = 'yearly'
                if date[1] != '':
                    query += ' AND month = ?'
                    data.append(int(date[1]))
                    duration = 'monthly'
                    if date[0] != '':
                        query += ' AND day = ?'
                        data.append(int(date[0]))
                        duration = 'daily'
            if data == []:
                return False, [], []

            query += ' AND account = ?'

            connect = sql.connect('database.db')
            cursor = connect.cursor()

            for index,value in enumerate(list_of_value):
                value = list(value)
                temp_data = data.copy()
                temp_data.append(value[3])
                cursor.execute(query,temp_data)

                row = cursor.fetchall()[0]
                total = row[0] if row and row[0] is not None else 0
                
                value[0] = index 
                base_value = float(value[5])
                value[5] = float(round(calculate_dict[value[4]][calculate_part[duration]] * base_value))
                value[4] = duration
                value[6] = total
                value[7] = (float(value[5]) - float(value[6]))
                res2.append(value)
                if value[6] > 0:
                    res[0].append(total)
                    res[3].append(value[3])
                res[1].append(value[3])
                res[2].append(value[5])
            #Ammount Total , Budget account, Budget total, amount account
            connect.close()
            return True, res, res2
        except Exception as e:
            return False, [], []
        finally:
            if 'connect' in locals():
                connect.close()
                
    def offline_budget_fetch(self,special_add_command='',data=[]):
        try:
            connect = sql.connect('database.db')
            cursor = connect.cursor()
            res = []
            query = 'SELECT * FROM budget WHERE 1=1'
            
            if special_add_command != '' and data != []:
                query += special_add_command
                cursor.execute(query,data)
            else:
                cursor.execute(query)
            temp = cursor.fetchall()
            for index,value in enumerate(temp):
                res.append((index+1,*value,0,0))
            return res
        except Exception as e:
            pass


class GUI:
    def __init__(self):
        #main config stuff
        self.account_list = []
        self.category_list =[]

        self.account_type = ['assets','liabilities','equity','revenue','expenses']

        #Check whether user use online or offline mode
        self.is_online = False

        #The ID value for Selection in trasanction page
        self.treeview_id = int
        self.treeview_selected_row = None
        self.treeview_selected_row_account = None

        #Budget ID
        self.treeview_selected_row_budget = None

        #Loading :()

api = API()
state = GUI()

#Functions to build pages acessed
def build_bootoption_page():
    bootoption_page_frame1 =  Frame(bootoption_page, background = light_dark)
    pack_center(bootoption_page,bootoption_page_frame1,light_dark)

    #Right frame aka the offline mode hehe
    bootoption_page_frame1_frame1 = Frame(bootoption_page_frame1, background = sub_lightdark)
    bootoption_page_frame1_frame1.pack(side='left',fill='both',expand=1,padx=20)

    bootoption_page_frame1_frame1_frame1 = Frame(bootoption_page_frame1_frame1, background = light_dark)
    bootoption_page_frame1_frame1_frame1.pack(side='top',fill='both',expand=1,padx=10,pady=10)

    bootoption_page_frame1_frame1_frame1_frame1 = Frame(bootoption_page_frame1_frame1_frame1, background = light_dark)
    bootoption_page_frame1_frame1_frame1_frame1.grid(column=0,row=0,sticky='nsew',pady=3,padx=(10,0))

    bootoption_page_frame1_frame1_frame1_frame1_label1 = Label(bootoption_page_frame1_frame1_frame1_frame1, background=light_dark, text= 'Offline', font=(custom_font,30),fg=error_color)
    bootoption_page_frame1_frame1_frame1_frame1_label1.pack(side='left')

    bootoption_page_frame1_frame1_frame1_frame1_label2 = Label(bootoption_page_frame1_frame1_frame1_frame1, background=light_dark, text= 'Mode', font=(custom_font,30),fg=text_color)
    bootoption_page_frame1_frame1_frame1_frame1_label2.pack(side='left')

    bootoption_page_frame1_frame1_frame1_label3 = Label(bootoption_page_frame1_frame1_frame1, background=light_dark, text= '- No internet required', font=(custom_font,20),fg=text_color)
    bootoption_page_frame1_frame1_frame1_label3.grid(column=0,row=1,sticky='nsw',padx=(30,10),columnspan=2)

    bootoption_page_frame1_frame1_frame1_label4 = Label(bootoption_page_frame1_frame1_frame1, background=light_dark, text= '- Data saved locally', font=(custom_font,20),fg=text_color)
    bootoption_page_frame1_frame1_frame1_label4.grid(column=0,row=2,sticky='nsw',padx=(30,10),columnspan=2)

    bootoption_page_frame1_frame2_frame1_label5 = Label(bootoption_page_frame1_frame1_frame1, background=light_dark, text= '- Data is truly safe against malicious attacks', font=(custom_font,20),fg=text_color)
    bootoption_page_frame1_frame2_frame1_label5.grid(column=0,row=3,sticky='nsw',padx=(30,10),columnspan=2)

    bootoption_page_frame1_frame1_frame1_label6 = Label(bootoption_page_frame1_frame1_frame1, background=light_dark, text= '- Data might corrupt', font=(custom_font,20),fg='#FFF200')
    bootoption_page_frame1_frame1_frame1_label6.grid(column=0,row=4,sticky='nsw',padx=(30,10),pady=(0,3),columnspan=2)

    bootoption_page_frame1_frame1_button1 = Button(bootoption_page_frame1_frame1,text='Use Offline Mode',foreground=text_color,background=light_dark,font=(custom_font,20,'bold'),command=offline_startup)
    bootoption_page_frame1_frame1_button1.pack(side='top',fill='both',expand=1,padx=10,pady=(0,10))

    #Left frame aka the online mode
    bootoption_page_frame1_frame2 = Frame(bootoption_page_frame1, background = sub_lightdark)
    bootoption_page_frame1_frame2.pack(side='left',fill='both',expand=1,padx=20)

    bootoption_page_frame1_frame2_frame1 = Frame(bootoption_page_frame1_frame2, background = light_dark)
    bootoption_page_frame1_frame2_frame1.pack(side='top',fill='both',expand=1,padx=10,pady=10)

    bootoption_page_frame1_frame2_frame1_frame1 = Frame(bootoption_page_frame1_frame2_frame1, background = light_dark)
    bootoption_page_frame1_frame2_frame1_frame1.grid(column=0,row=0,sticky='nsew',pady=3,padx=(10,0))

    bootoption_page_frame1_frame2_frame1_frame1_label1 = Label(bootoption_page_frame1_frame2_frame1_frame1, background=light_dark, text= 'Online', font=(custom_font,30),fg=success_color)
    bootoption_page_frame1_frame2_frame1_frame1_label1.pack(side='left')

    bootoption_page_frame1_frame2_frame1_frame1_label2 = Label(bootoption_page_frame1_frame2_frame1_frame1, background=light_dark, text= 'Mode', font=(custom_font,30),fg=text_color)
    bootoption_page_frame1_frame2_frame1_frame1_label2.pack(side='left')

    bootoption_page_frame1_frame2_frame1_frame1_label3 = Label(bootoption_page_frame1_frame2_frame1_frame1, background=light_dark, text= '(under development :D)', font=(custom_font,30),fg='#FFF200')
    bootoption_page_frame1_frame2_frame1_frame1_label3.pack(side='left')

    bootoption_page_frame1_frame2_frame1_label3 = Label(bootoption_page_frame1_frame2_frame1, background=light_dark, text= '- Syncs with cloud/server', font=(custom_font,20),fg=text_color)
    bootoption_page_frame1_frame2_frame1_label3.grid(column=0,row=1,sticky='nsw',padx=(30,10),columnspan=2)

    bootoption_page_frame1_frame2_frame1_label4 = Label(bootoption_page_frame1_frame2_frame1, background=light_dark, text= '- Requires internet connection', font=(custom_font,20),fg=text_color)
    bootoption_page_frame1_frame2_frame1_label4.grid(column=0,row=2,sticky='nsw',padx=(30,10),columnspan=2)

    bootoption_page_frame1_frame2_frame1_label5 = Label(bootoption_page_frame1_frame2_frame1, background=light_dark, text= '- Data can be accessed through different PC', font=(custom_font,20),fg=text_color)
    bootoption_page_frame1_frame2_frame1_label5.grid(column=0,row=3,sticky='nsw',padx=(30,10),columnspan=2)

    bootoption_page_frame1_frame2_frame1_label6 = Label(bootoption_page_frame1_frame2_frame1, background=light_dark, text= '- Server can be down', font=(custom_font,20),fg='#FFF200')
    bootoption_page_frame1_frame2_frame1_label6.grid(column=0,row=4,sticky='nsw',padx=(30,10),pady=(0,3),columnspan=2)

    bootoption_page_frame1_frame2_button1 = Button(bootoption_page_frame1_frame2,text='Use Online Mode',foreground=text_color,background=light_dark,font=(custom_font,20,'bold'))
    bootoption_page_frame1_frame2_button1.pack(side='top',fill='both',expand=1,padx=10,pady=(0,10))
def build_signup_page():
    signuppage_frame = Frame(signup_page, background=sub_lightdark)
    pack_center(signup_page,signuppage_frame,light_dark)
    signuppage_brand = Label(signup_page,text=' Budgit',compound='left',background=light_dark,font=('monogram',24),fg=text_color,image=logo_photo)
    signuppage_brand.place(anchor='ne',x=130,y=10)

    signuppage_subframe = Frame(signuppage_frame, background=sub_lightdark)
    signuppage_subframe.pack(side='top',padx=20,pady=20)

    signuppage_subframe_title1 = Label(signuppage_subframe, background=sub_lightdark, text= 'Create an account', font=(custom_font,50),fg=text_color)
    signuppage_subframe_title1.grid(column=0,row=0,sticky='nsw',columnspan=2,pady=20)
    signuppage_subframe.grid_rowconfigure(0,weight=0)

    signuppage_subframe_frame1 = Frame(signuppage_subframe,background=sub_lightdark)
    signuppage_subframe_frame1.grid(column=0,row=1,sticky='nsew',pady=(0,10),columnspan=2)
    signuppage_subframe_text1 = Label(signuppage_subframe_frame1, background=sub_lightdark, text= 'Already have an account?',justify = 'left', font=(custom_font,20),fg=sub_textcolor)
    signuppage_subframe_text1.pack(side='left')
    signuppage_subframe_button4 = Label(signuppage_subframe_frame1, background=sub_lightdark, text = 'Login',justify = 'left', font=(custom_font, 20),fg=main_color )
    signuppage_subframe_button4.bind('<Enter>',lambda event :signuppage_subframe_button4.configure(font=(custom_font, 20, 'underline')))
    signuppage_subframe_button4.bind('<Leave>',lambda event :signuppage_subframe_button4.configure(font=(custom_font, 20)))
    signuppage_subframe_button4.bind ('<Button-1>', lambda event : load_page('login_page'))
    signuppage_subframe_button4.pack(side='left')

    signuppage_subframe_text2 = Label(signuppage_subframe, background=sub_lightdark, font=(custom_font,16),fg=error_color,text='',justify='left')
    signuppage_subframe_text2.grid(column=0,row=2,sticky='nsw',columnspan=2,pady=(0,5))

    signuppage_subframe_entry1 = Entry(signuppage_subframe, background = light_dark, fg = sub_textcolor,font=('monogram',20))
    signuppage_subframe_entry1.insert(0,'Email')
    signuppage_subframe_entry1.bind('<FocusIn>', lambda event: entry_text(signuppage_subframe_entry1,['\u200BEmail']))
    signuppage_subframe_entry1.bind('<FocusOut>', lambda event: entry_text(signuppage_subframe_entry1,['\u200BEmail'],True,'\u200BEmail'))
    signuppage_subframe_entry1.grid(column=0,row=3,sticky='nsew',pady=(0,10),columnspan=2,ipady=10)

    signuppage_subframe_entry2 = Entry(signuppage_subframe, background = light_dark, fg = sub_textcolor,font=('monogram',20))
    signuppage_subframe_entry2.insert(0,'Password')
    signuppage_subframe_entry2.bind('<FocusIn>', lambda event: entry_text(signuppage_subframe_entry2,['\u200BPassword'],password=True))
    signuppage_subframe_entry2.bind('<FocusOut>', lambda event: entry_text(signuppage_subframe_entry2,['\u200BPassword'],True,'\u200BPassword'))
    signuppage_subframe_entry2.grid(column=0,row=4,sticky='nsew',pady=(0,10),columnspan=2,ipady=10)

    signuppage_subframe_entry3 = Entry(signuppage_subframe, background = light_dark, fg = sub_textcolor,font=('monogram',20))
    signuppage_subframe_entry3.insert(0,'Confirm Password')
    signuppage_subframe_entry3.bind('<FocusIn>', lambda event: entry_text(signuppage_subframe_entry3,['\u200BConfirm Password'],password=True))
    signuppage_subframe_entry3.bind('<FocusOut>', lambda event: entry_text(signuppage_subframe_entry3,['\u200BConfirm Password'],True,'\u200BConfirm Password'))
    signuppage_subframe_entry3.grid(column=0,row=5,sticky='nsew',pady=(0,10),columnspan=2,ipady=10)

    signuppage_subframe_checkbox1 = ttk.Checkbutton(signuppage_subframe, text='Remember me ', style = 'Custom.TCheckbutton', variable = remember_var)
    signuppage_subframe_checkbox1.grid(column=0,row=6,sticky='nsew',pady=(5,10),columnspan=2)

    signuppage_subframe_button1 = Button(signuppage_subframe,text='Create account',foreground=text_color,background=light_dark,font=(custom_font,20,'bold'),command= lambda: api.online_signup_email(email_widget=signuppage_subframe_entry1,password_widget=signuppage_subframe_entry2, error_msg_widget=signuppage_subframe_text2, confirm_password_widget=signuppage_subframe_entry3))
    signuppage_subframe_button1.grid(column=0,row=7,sticky='nsew',pady=(30,0),columnspan=2,ipady=10)

    signuppage_subframe_canvas1 = Canvas(signuppage_subframe,background=sub_lightdark,highlightthickness=0,height=20)
    signuppage_subframe_canvas1.create_line(0,10,450,10,fill='#444', width=2)
    signuppage_subframe_canvas1.create_rectangle(140,0,290,20,fill=sub_lightdark,outline=sub_lightdark)
    signuppage_subframe_canvas1.create_text(217,10,fill=text_color,text='Or register with',font=(custom_font,15))
    signuppage_subframe_canvas1.grid(column=0,row=8,sticky='nsew',pady=25,columnspan=2)

    signuppage_subframe_button2 = Button(signuppage_subframe,text='Google', foreground=text_color,background=light_dark, font=(custom_font,20,'bold'),image=logo_google_photo )
    signuppage_subframe_button2.grid(column=0,row=9,sticky='nsew',pady=10,padx=(0,5), ipady=10)

    signuppage_subframe_button3 = Button(signuppage_subframe,text='Github', foreground=text_color,background=light_dark, font=(custom_font,20,'bold'),image=logo_github_photo )
    signuppage_subframe_button3.grid(column=1,row=9,sticky='nsew',pady=10,padx=(0,5), ipady=10)
def build_signup_initialise_page():

    def renumber_list(treeview,class_,list_name,types):
        lists = getattr(class_,list_name)
        treeview.delete(*treeview.get_children())
        for i in range(len(lists)):
            lists[i]['no'] = i
            treeview.insert('','end',values=(lists[i]['no']+1,lists[i]['type'], lists[i][types]))
    def add_default_list(treeview,class_,list_name,types,list_to_add):
        lists = getattr(class_,list_name)
        for dicts in list_to_add:
            lists.append({'no':len(lists),'type':dicts['type'] ,types:dicts['category']})
            treeview.insert('','end',values=(len(lists),dicts['type'],dicts['category']))
    def remove_var_fromlist(treeview,class_,list_name,entry_widget,types,error_widget):
        targeted_account = entry_widget.get().lower()
        lists = getattr(class_,list_name)
        for i in range(len(lists)):
            if lists[i][types] == targeted_account:
                del lists[i]
                entry_widget.delete(0,END)
                renumber_list(treeview,class_,list_name,types)
                return
        
        error_widget.configure(text=f'{targeted_account} is not found in the {types} list')
    def add_var_tolist(treeview,class_,list_name,entry_widget,combo_box_widget,types,error_widget):
        lists = getattr(class_,list_name)
        list_size = len(lists)
        targeted_account = entry_widget.get().lower()
        targeted_type = combo_box_widget.get()

        if len(targeted_type) == 0 or targeted_account == 'insert here' :
            error_widget.configure(text=f'Incomplete input')
            return

        if len(targeted_account) >= 16 :
            entry_widget.delete(0,END)
            error_widget.configure(text=f'{targeted_account} is too long for {types} list, maximum 16 letter')
            return

        for i in range(list_size):
            if targeted_account == lists[i][types]:
                entry_widget.delete(0,END)
                error_widget.configure(text=f'{targeted_account} is already in the {types} list')
                return

        lists.append({'no': (list_size ),'type':targeted_type,types: targeted_account})
        treeview.insert('','end',values=(lists[list_size]['no']+1,targeted_type,targeted_account))
        entry_widget.delete(0,END)
        error_widget.configure(text='')
    def offline_setup():
        lists = []
        for parent in signup_initialise_page_mainframe_frame1_innerframe1_treeview1.get_children():
            lists.append(signup_initialise_page_mainframe_frame1_innerframe1_treeview1.item(parent)['values'])

        api.offline_confirm_setup(lists=lists,changed_format=[2,1],convert=1)
        load_page('accounting_page')

    signup_initialise_page_mainframe_brand1 = Label(signup_initialise_page,text=' Budgit',compound='left',background=light_dark,font=('monogram',24),fg=text_color,image=logo_photo)
    signup_initialise_page_mainframe_brand1.place(anchor='ne',x=130,y=10)

    signup_initialise_page_mainframe = Frame(signup_initialise_page, background=sub_lightdark)
    signup_initialise_page_mainframe.pack(side='top',fill='both',expand=1,padx=100,pady=100)

    signup_initialise_page_mainframe_label1 = Label(signup_initialise_page_mainframe, background=sub_lightdark, text= 'Initial Setup', font=(custom_font,30),fg=text_color)
    signup_initialise_page_mainframe_label1.grid(column=0,row=0,columnspan=3,sticky='nsew',pady=3)

    #Frane 1
    signup_initialise_page_mainframe_frame1 = Frame(signup_initialise_page_mainframe, background=mid_dark)
    signup_initialise_page_mainframe_frame1.grid(column=0,row=1,sticky='nsew',padx=20,pady=(0,20),rowspan=2)

    signup_initialise_page_mainframe_frame1_innerframe1 = Frame(signup_initialise_page_mainframe_frame1, background=mid_dark)
    signup_initialise_page_mainframe_frame1_innerframe1.pack(side='top',fill='both',expand=1, padx=5,pady=5)

    signup_initialise_page_mainframe_frame1_innerframe1_label1 = Label(signup_initialise_page_mainframe_frame1_innerframe1, background=mid_dark, text= 'Account List', font=(custom_font,30),fg=text_color)
    signup_initialise_page_mainframe_frame1_innerframe1_label1.grid(column=0,row=0,sticky='nsw',columnspan=2)

    signup_initialise_page_mainframe_frame1_innerframe1_label2 = Label(signup_initialise_page_mainframe_frame1_innerframe1, background=mid_dark, text= 'Below are the default', font=(custom_font,16),fg=sub_textcolor)
    signup_initialise_page_mainframe_frame1_innerframe1_label2.grid(column=0,row=1,sticky='nw',columnspan=2)

    signup_initialise_page_mainframe_frame1_innerframe1_label3 = Label(signup_initialise_page_mainframe_frame1_innerframe1, background=mid_dark, text= '', font=(custom_font,16),fg=error_color)
    signup_initialise_page_mainframe_frame1_innerframe1_label3.grid(column=0,row=2,sticky='nw',columnspan=2)

    account_treeview = ['No.','Account Type','Account']
    account_yscrollbar = ttk.Scrollbar(signup_initialise_page_mainframe_frame1_innerframe1)
    account_yscrollbar.grid(column=1,row=3,sticky='nsw')
    signup_initialise_page_mainframe_frame1_innerframe1_treeview1 = ttk.Treeview(signup_initialise_page_mainframe_frame1_innerframe1,columns=account_treeview,show='headings',yscrollcommand=account_yscrollbar.set)
    signup_initialise_page_mainframe_frame1_innerframe1_treeview1.grid(column=0,row=3,sticky='nsew')
    account_yscrollbar.configure(command = signup_initialise_page_mainframe_frame1_innerframe1_treeview1.yview)

    signup_initialise_page_mainframe_frame1_innerframe1_treeview1.heading('No.',text='No.')
    signup_initialise_page_mainframe_frame1_innerframe1_treeview1.column('No.',stretch=True,minwidth=30,width=30)

    signup_initialise_page_mainframe_frame1_innerframe1_treeview1.heading('Account Type',text='Account Type')
    signup_initialise_page_mainframe_frame1_innerframe1_treeview1.column('Account Type',stretch=True,minwidth=50,width=100)

    signup_initialise_page_mainframe_frame1_innerframe1_treeview1.heading('Account',text='Account')
    signup_initialise_page_mainframe_frame1_innerframe1_treeview1.column('Account',stretch=True,minwidth=50,width=100)
    add_default_list(signup_initialise_page_mainframe_frame1_innerframe1_treeview1,state,'category_list','category',[{'type':'assets','category':'cash'},{'type':'liabilities','category':'loans'},{'type':'equity','category':'capital'},{'type':'revenue','category':'income'},{'type':'expenses','category':'groceries'}])

    signup_initialise_page_mainframe_frame1_innerframe1_entryframe1 = Frame(signup_initialise_page_mainframe_frame1_innerframe1, background=sub_lightdark)
    signup_initialise_page_mainframe_frame1_innerframe1_entryframe1.grid(column=0,row=4,sticky='nsew',pady=(5,0),columnspan=2,ipady=10)

    signup_initialise_page_mainframe_frame1_innerframe1_entryframe1_label1 = Label(signup_initialise_page_mainframe_frame1_innerframe1_entryframe1, background=sub_lightdark, text= 'Account Type', font=(custom_font,20),fg=text_color)
    signup_initialise_page_mainframe_frame1_innerframe1_entryframe1_label1.grid(column=0,row=0,sticky='nsw',padx=5)

    signup_initialise_page_mainframe_frame1_innerframe1_entryframe1_label2= Label(signup_initialise_page_mainframe_frame1_innerframe1_entryframe1, background=sub_lightdark, text= 'Account', font=(custom_font,20),fg=text_color)
    signup_initialise_page_mainframe_frame1_innerframe1_entryframe1_label2.grid(column=1,row=0,sticky='nsw',padx=(0,5))

    signup_initialise_page_mainframe_frame1_innerframe1_entryframe1_entry1 = Entry(signup_initialise_page_mainframe_frame1_innerframe1_entryframe1, background = light_dark, fg = sub_textcolor,font=('monogram',20))
    signup_initialise_page_mainframe_frame1_innerframe1_entryframe1_entry1.insert(0,'\u200BInsert Here')
    signup_initialise_page_mainframe_frame1_innerframe1_entryframe1_entry1.bind('<FocusIn>', lambda event: entry_text(signup_initialise_page_mainframe_frame1_innerframe1_entryframe1_entry1,['\u200BInsert Here']))
    signup_initialise_page_mainframe_frame1_innerframe1_entryframe1_entry1.bind('<FocusOut>', lambda event: entry_text(signup_initialise_page_mainframe_frame1_innerframe1_entryframe1_entry1,['\u200BInsert Here'],True,'\u200BInsert Here'))
    signup_initialise_page_mainframe_frame1_innerframe1_entryframe1_entry1.grid(column=1,row=1,sticky='nsew',padx=5)


    #VARIABLE IMPORTANT TO CHANGE ! for online or offline mode :)
    signup_initialise_page_mainframe_frame1_innerframe1_entryframe1_combobox1 = ttk.Combobox(signup_initialise_page_mainframe_frame1_innerframe1_entryframe1, background = light_dark, foreground = text_color,font=('monogram',20),state='readonly')
    signup_initialise_page_mainframe_frame1_innerframe1_entryframe1_combobox1.grid(column=0,row=1,sticky='nsew',padx=(5,0))
    #End

    signup_initialise_page_mainframe_frame1_innerframe1_entryframe1.grid_columnconfigure((0,1), weight=1)

    signup_initialise_page_mainframe_frame1_innerframe1_buttonframe1 = Frame(signup_initialise_page_mainframe_frame1_innerframe1, background=sub_lightdark)
    signup_initialise_page_mainframe_frame1_innerframe1_buttonframe1.grid(column=0,row=5,sticky='nsew',columnspan=2,pady=(5,0))

    signup_initialise_page_mainframe_frame1_innerframe1_button1 = Button(signup_initialise_page_mainframe_frame1_innerframe1_buttonframe1,text='Remove',foreground=text_color,background=light_dark,font=(custom_font,20,'bold'),command= lambda:remove_var_fromlist(signup_initialise_page_mainframe_frame1_innerframe1_treeview1,state,'category_list',signup_initialise_page_mainframe_frame1_innerframe1_entryframe1_entry1,'category',signup_initialise_page_mainframe_frame1_innerframe1_label3))
    signup_initialise_page_mainframe_frame1_innerframe1_button1.grid(column=0,row=0,sticky='nsew',ipady=10)

    signup_initialise_page_mainframe_frame1_innerframe1_button2 = Button(signup_initialise_page_mainframe_frame1_innerframe1_buttonframe1,text='Add',foreground=text_color,background=light_dark,font=(custom_font,20,'bold'),command= lambda: add_var_tolist(signup_initialise_page_mainframe_frame1_innerframe1_treeview1,state,'category_list',signup_initialise_page_mainframe_frame1_innerframe1_entryframe1_entry1,signup_initialise_page_mainframe_frame1_innerframe1_entryframe1_combobox1,'category',signup_initialise_page_mainframe_frame1_innerframe1_label3))
    signup_initialise_page_mainframe_frame1_innerframe1_button2.grid(column=1,row=0,sticky='nsew',ipady=10)

    signup_initialise_page_mainframe_frame1_innerframe1_buttonframe1.grid_columnconfigure((0,1),weight=1,uniform='a')
    signup_initialise_page_mainframe_frame1_innerframe1_buttonframe1.grid_rowconfigure(0,weight=1,uniform='a')

    signup_initialise_page_mainframe_frame1_innerframe1.grid_rowconfigure(3,weight=1)
    signup_initialise_page_mainframe_frame1_innerframe1.grid_columnconfigure(0,weight=1)

    #fRAME 2
    signup_initialise_page_mainframe_frame2 = Frame(signup_initialise_page_mainframe, background=mid_dark)
    signup_initialise_page_mainframe_frame2.grid(column=1,row=1,sticky='nsew',pady=(0,5),padx=(0,20))

    signup_initialise_page_mainframe_frame2_innerframe1 = Frame(signup_initialise_page_mainframe_frame2, background=mid_dark)
    signup_initialise_page_mainframe_frame2_innerframe1.pack(side='top',fill='both',expand=1, padx=5,pady=5)

    signup_initialise_page_mainframe_frame2_innerframe1_label1 = Label(signup_initialise_page_mainframe_frame2_innerframe1, background=mid_dark, text= 'User Profile', font=(custom_font,30),fg=text_color)
    signup_initialise_page_mainframe_frame2_innerframe1_label1.grid(column=0,row=0,sticky='nsw',columnspan=2)

    signup_initialise_page_mainframe_frame2_innerframe1_label2 = Label(signup_initialise_page_mainframe_frame2_innerframe1, background=mid_dark, text= 'Below is the default', font=(custom_font,16),fg=sub_textcolor)
    signup_initialise_page_mainframe_frame2_innerframe1_label2.grid(column=0,row=1,sticky='nw',columnspan=2)

    signup_initialise_page_mainframe_frame2_innerframe1_label3 = Label(signup_initialise_page_mainframe_frame2_innerframe1, background=mid_dark, text= 'currency:', font=(custom_font,20),fg=text_color)
    signup_initialise_page_mainframe_frame2_innerframe1_label3.grid(column=0,row=2,sticky='nws')

    #Buttons for done and back yeah hehe
    signup_initialise_page_mainframe_frame4 = Frame(signup_initialise_page_mainframe, background=sub_lightdark)
    signup_initialise_page_mainframe_frame4.grid(column=1,row=2,sticky='nsew',pady=(0,20),padx=(0,20),columnspan=2)

    signup_initialise_page_mainframe_button1 = Button(signup_initialise_page_mainframe_frame4,text='Back',foreground=text_color,background=light_dark,font=(custom_font,20,'bold'))
    signup_initialise_page_mainframe_button1.pack(side='left',fill='both',expand=1,ipady=10)

    signup_initialise_page_mainframe_button2 = Button(signup_initialise_page_mainframe_frame4,text='Confirm',foreground=text_color,background=light_dark,font=(custom_font,20,'bold'))
    signup_initialise_page_mainframe_button2.pack(side='left',fill='both',expand=1,ipady=10)

    signup_initialise_page_mainframe.grid_columnconfigure((0,1),weight=1)
    signup_initialise_page_mainframe.grid_rowconfigure(1,weight=1)


    #Switching from offline and online configuration
    is_online = getattr(state,'is_online')
    if not is_online:
        c = api.offline_fetch_account()
        type_list = []
        for i in c:
            type_list.append(i[0])
        signup_initialise_page_mainframe_frame1_innerframe1_entryframe1_combobox1.configure(values=type_list)

        #button command
        signup_initialise_page_mainframe_button2.configure(command= offline_setup)
    else:
        print('hello world')
def build_login_page(auto_login_email=None,auto_login_password=None):
    loginpage_frame = Frame(login_page, background=sub_lightdark)
    pack_center(login_page,loginpage_frame,light_dark)
    loginpage_brand = Label(login_page,text=' Budgit',compound='left',background=light_dark,font=('monogram',24),fg=text_color,image=logo_photo)
    loginpage_brand.place(anchor='ne',x=130,y=10)

    loginpage_subframe = Frame(loginpage_frame, background=sub_lightdark,border=5,borderwidth=5)
    loginpage_subframe.pack(side='top',padx=20,pady=20)

    loginpage_subframe_title1 = Label(loginpage_subframe, background=sub_lightdark, text= 'Welcome Back!', font=(custom_font,50),fg=text_color)
    loginpage_subframe_title1.grid(column=0,row=0,sticky='nsw',columnspan=2,pady=20)
    loginpage_subframe.grid_rowconfigure(0,weight=0)

    loginpage_subframe_frame1 = Frame(loginpage_subframe,background=sub_lightdark)
    loginpage_subframe_frame1.grid(column=0,row=1,sticky='nsew',pady=(0,10),columnspan=2)
    loginpage_subframe_text1 = Label(loginpage_subframe_frame1, background=sub_lightdark, text= 'Dont have an account?',justify = 'left', font=(custom_font,20),fg=sub_textcolor)
    loginpage_subframe_text1.pack(side='left')
    loginpage_subframe_button4 = Label(loginpage_subframe_frame1, background=sub_lightdark, text = 'Signup',justify = 'left', font=(custom_font, 20),fg=main_color )
    loginpage_subframe_button4.bind('<Enter>',lambda event :loginpage_subframe_button4.configure(font=(custom_font, 20, 'underline')))
    loginpage_subframe_button4.bind('<Leave>',lambda event :loginpage_subframe_button4.configure(font=(custom_font, 20)))
    loginpage_subframe_button4.bind ('<Button-1>', lambda event : load_page('signup_page'))
    loginpage_subframe_button4.pack(side='left')

    loginpage_subframe_text2 = Label(loginpage_subframe, background=sub_lightdark, font=(custom_font,16),fg=error_color,text='',justify='left')
    loginpage_subframe_text2.grid(column=0,row=2,sticky='nsw',columnspan=2,pady=(0,5))

    loginpage_subframe_entry1 = Entry(loginpage_subframe, background = light_dark, fg = sub_lightdark,font=('monogram',20))
    loginpage_subframe_entry1.insert(0,'Email')
    loginpage_subframe_entry1.bind('<FocusIn>', lambda event: entry_text(loginpage_subframe_entry1,['\u200BEmail']))
    loginpage_subframe_entry1.bind('<FocusOut>', lambda event: entry_text(loginpage_subframe_entry1,['\u200BEmail'],True,'\u200BEmail'))
    loginpage_subframe_entry1.grid(column=0,row=3,sticky='nsew',pady=(0,10),columnspan=2,ipady=10)

    loginpage_subframe_entry2 = Entry(loginpage_subframe, background = light_dark, fg = sub_lightdark,font=('monogram',20))
    loginpage_subframe_entry2.insert(0,'Password')
    loginpage_subframe_entry2.bind('<FocusIn>', lambda event: entry_text(loginpage_subframe_entry2,['\u200BPassword'],password=True))
    loginpage_subframe_entry2.bind('<FocusOut>', lambda event: entry_text(loginpage_subframe_entry2,['\u200BPassword'],True,'\u200BPassword'))
    loginpage_subframe_entry2.grid(column=0,row=4,sticky='nsew',pady=(0,10),columnspan=2,ipady=10)

    loginpage_subframe_checkbox1 = ttk.Checkbutton(loginpage_subframe, text='Remember me ', style = 'Custom.TCheckbutton', variable = remember_var)
    loginpage_subframe_checkbox1.grid(column=0,row=5,sticky='nsew',pady=(5,10),columnspan=2)

    loginpage_subframe_button1 = Button(loginpage_subframe,text='Login',foreground=text_color,background=light_dark,font=(custom_font,20,'bold'),command= lambda: api.online_login_email(email_widget=loginpage_subframe_entry1,password_widget=loginpage_subframe_entry2, error_msg_widget=loginpage_subframe_text2,remember_me_var=remember_var))
    loginpage_subframe_button1.grid(column=0,row=6,sticky='nsew',pady=(30,0),columnspan=2,ipady=10)

    loginpage_subframe_canvas1 = Canvas(loginpage_subframe,background=sub_lightdark,highlightthickness=0,height=20)
    loginpage_subframe_canvas1.create_line(0,10,450,10,fill='#444', width=2)
    loginpage_subframe_canvas1.create_rectangle(105,0,270,20,fill=sub_lightdark,outline=sub_lightdark)
    loginpage_subframe_canvas1.create_text(190,10,fill=text_color,text='Or register with',font=(custom_font,15))
    loginpage_subframe_canvas1.grid(column=0,row=7,sticky='nsew',pady=25,columnspan=2)

    loginpage_subframe_button2 = Button(loginpage_subframe,text='Google', foreground=text_color,background=light_dark, font=(custom_font,20,'bold'),image=logo_google_photo )
    loginpage_subframe_button2.grid(column=0,row=8,sticky='nsew',pady=10,padx=(0,5), ipady=10)

    loginpage_subframe_button3 = Button(loginpage_subframe,text='Github', foreground=text_color,background=light_dark, font=(custom_font,20,'bold'),image=logo_github_photo )
    loginpage_subframe_button3.grid(column=1,row=8,sticky='nsew',pady=10,padx=(0,5), ipady=10)

    if auto_login_email and auto_login_password:
        loginpage_subframe_entry1.delete(0, END)
        loginpage_subframe_entry2.delete(0, END)
        loginpage_subframe_entry1.configure(foreground=text_color)
        loginpage_subframe_entry2.configure(foreground=text_color)

        loginpage_subframe_entry1.insert(0, str(auto_login_email))
        loginpage_subframe_entry2.insert(0, str(auto_login_password))
        loginpage_subframe_button1.invoke()
def build_accounting_page():
    def accountingpage_leftside_button_function(widget_list=list,list_fg=str,targeted_widget=Widget,targeted_fg=str,targeted_frame=None,frame_list=None):
        for widget in widget_list:
            if widget != targeted_widget:
                widget.configure(fg = list_fg)
            else:
                widget.configure(fg = targeted_fg)

        if targeted_frame and frame_list:
            for frame in frame_list:
                if frame == targeted_frame:
                    frame.pack(side='top', padx = 20, pady=20,fill='both',expand=1)
                else:
                    frame.pack_forget()

        #Category setup function
        if targeted_frame == accountingpage_subframe2_frame3:
            category_treeview.delete(*category_treeview.get_children())

            if getattr(state,'is_online') == False :
                try:
                    lists = api.offline_fetch_accounts()
                    total = 0.0
                    for index,row in enumerate(lists):
                        category_treeview.insert('','end',values=[*[index+1],*row])
                        total += float(row[4])
                    category_data_label1.configure(text=len(lists))
                    category_data_label2.configure(text=str(total))
                except Exception as e:
                    print(e)
            return

        #accounting Transaction setup Function
        elif targeted_frame == accountingpage_subframe2_frame2:
            transaction_label_frame.grid_forget()
            transaction_button_frame.grid(column=0,row=0,sticky='nsew')
            transaction_data_frame.grid_forget()

            transaction_treeview.delete(*transaction_treeview.get_children())
            amount_label.configure(text='0.0')
            transaction_label.configure(text='0')
            date_widgets.configure(text='00-00-0000')
            
        elif targeted_frame == accountingpage_subframe2_frame4:
            budget_treeview.delete(budget_treeview.get_children())
            res = api.offline_budget_fetch()
            for i in res:
                budget_treeview.insert('','end',values=i)

            budget_ax1.clear()
            budget_ax2.clear()
            budget_ax1.pie([100], labels=['None'],textprops={'fontsize': 37},autopct='%1.1f%%',colors=['gray'])
            budget_ax2.pie([100], labels=['None'],textprops={'fontsize': 37},autopct='%1.1f%%',colors=['gray'])

            budget_fg1.draw_idle()
            budget_fg2.draw_idle()

            budget_value.configure(text='0')
            budget_value2.configure(text='0')
            budget_percentagediff.configure(text='0%')
            budget_cmb1.set('')
            budget_cmb1.configure(values=[])
            budget_cmb2.set('')
            budget_cmb2.configure(values=[])
            budget_cmb3.set('')
            budget_frame1.pack(side='top',fill='both',expand=1)
            budget_frame2.pack_forget()
            budget_frame3.pack_forget()
            
            
    #Main tabs for the accounting page dividing button to stuff :)
    accountingpage_mainframe1 = Frame(accounting_page,background = light_dark,width=250)
    accountingpage_mainframe1.grid(row=0,column=0,sticky='nsew')
    accountingpage_mainframe1.grid_propagate(False)
    accountingpage_mainframe1.pack_propagate(False)

    accountingpage_mainframe2 = Frame(accounting_page,background = sub_lightdark)
    accountingpage_mainframe2.grid(row=0, column = 1, sticky='nsew')
    accountingpage_mainframe2.grid_propagate(False)
    accountingpage_mainframe2.pack_propagate(False)

    accounting_page.grid_columnconfigure(0, weight = 0)
    accounting_page.grid_columnconfigure(1, weight = 4)
    accounting_page.grid_rowconfigure(0, weight=1)

    #right side of the frame , aka the frames to access the the stuff inside the frames

    #Dashboard page
    accountingpage_subframe2_frame1 = Frame(accountingpage_mainframe2,background=sub_maincolor)

    #Transactions page
    accountingpage_subframe2_frame2 = Frame(accountingpage_mainframe2,background=light_dark)
    transaction_treeview, transaction_error_msg,transaction_label_frame,transaction_button_frame,transaction_data_frame,func,amount_label,transaction_label,date_widgets = build_accounting_page_transaction(accountingpage_subframe2_frame2)

    #Category page
    accountingpage_subframe2_frame3 = Frame(accountingpage_mainframe2,background='white')
    category_treeview,category_data_label1,category_data_label2 = build_accounting_page_category(accountingpage_subframe2_frame3)

    accountingpage_subframe2_frame4 = Frame(accountingpage_mainframe2,background=light_dark)
    budget_treeview,budget_ax1,budget_fg1,budget_ax2,budget_fg2,budget_value,budget_value2,budget_percentagediff,budget_cmb1,budget_cmb2,budget_cmb3,budget_frame1,budget_frame2,budget_frame3 = build_accounting_page_budget(accountingpage_subframe2_frame4)

    accountingpage_subframe2_frame5 = Frame(accountingpage_mainframe2,background=sub_maincolor)

    accountingpage_subframe2_frame6 = Frame(accountingpage_mainframe2,background=sub_maincolor)

    #page list
    page_list = [accountingpage_subframe2_frame1,accountingpage_subframe2_frame2,accountingpage_subframe2_frame3,accountingpage_subframe2_frame4,accountingpage_subframe2_frame5,accountingpage_subframe2_frame6]

    #left side of the frame , aka the buttons to access the windows
    accountingpage_brand = Label(accountingpage_mainframe1,text=' Budgit',compound='left',background=light_dark,font=('monogram',24),fg=text_color)
    accountingpage_brand.place(anchor='nw',x=30,y=10)

    accountingpage_subframe1 = Frame(accountingpage_mainframe1, background=light_dark)
    accountingpage_subframe1.pack(side='top',pady=130, fill='x',padx=[30,0])

    accountingpage_subframe1_label1 = Label(accountingpage_subframe1,text='MAIN',background=light_dark,compound='left',font=('monogram',24),fg=sub_textcolor)
    accountingpage_subframe1_label1.grid(row=0, column=1, sticky='nsw',pady=(0,20))

    accountingpage_subframe1_label2 = Label(accountingpage_subframe1,text=' Dashboard',background=light_dark,compound='left',font=('monogram',24),fg=text_color, image = dashboard_photo)
    accountingpage_subframe1_label2.grid(row=1, column=1, sticky='nsw',pady=(0,20))
    accountingpage_subframe1_label2.bind('<Enter>',lambda event :accountingpage_subframe1_label2.configure(font=(custom_font, 24, 'bold')))
    accountingpage_subframe1_label2.bind('<Leave>',lambda event :accountingpage_subframe1_label2.configure(font=(custom_font, 24)))
    accountingpage_subframe1_label2.bind ('<Button-1>', lambda event : accountingpage_leftside_button_function(widget_list = [accountingpage_subframe1_label2,accountingpage_subframe1_label3,accountingpage_subframe1_label4,accountingpage_subframe1_label5,accountingpage_subframe1_label6,accountingpage_subframe1_label8],list_fg=text_color, targeted_widget=accountingpage_subframe1_label2,targeted_fg=sub_maincolor, targeted_frame=accountingpage_subframe2_frame1, frame_list=page_list))

    accountingpage_subframe1_label3 = Label(accountingpage_subframe1,text=' Transactions',background=light_dark,compound='left',font=('monogram',24),fg=text_color, image = transaction_photo)
    accountingpage_subframe1_label3.grid(row=2, column=1, sticky='nsw',pady=(0,20))
    accountingpage_subframe1_label3.bind('<Enter>',lambda event :accountingpage_subframe1_label3.configure(font=(custom_font, 24, 'bold')))
    accountingpage_subframe1_label3.bind('<Leave>',lambda event :accountingpage_subframe1_label3.configure(font=(custom_font, 24)))
    accountingpage_subframe1_label3.bind ('<Button-1>', lambda event : accountingpage_leftside_button_function(widget_list = [accountingpage_subframe1_label2,accountingpage_subframe1_label3,accountingpage_subframe1_label4,accountingpage_subframe1_label5,accountingpage_subframe1_label6,accountingpage_subframe1_label8],list_fg=text_color, targeted_widget=accountingpage_subframe1_label3,targeted_fg=sub_maincolor, targeted_frame=accountingpage_subframe2_frame2, frame_list=page_list))

    accountingpage_subframe1_label4 = Label(accountingpage_subframe1,text=' Category',background=light_dark,compound='left',font=('monogram',24),fg=text_color, image = wallet_photo)
    accountingpage_subframe1_label4.grid(row=3, column=1, sticky='nsw',pady=(0,20))
    accountingpage_subframe1_label4.bind('<Enter>',lambda event :accountingpage_subframe1_label4.configure(font=(custom_font, 24, 'bold')))
    accountingpage_subframe1_label4.bind('<Leave>',lambda event :accountingpage_subframe1_label4.configure(font=(custom_font, 24)))
    accountingpage_subframe1_label4.bind ('<Button-1>', lambda event : accountingpage_leftside_button_function(widget_list = [accountingpage_subframe1_label2,accountingpage_subframe1_label3,accountingpage_subframe1_label4,accountingpage_subframe1_label5,accountingpage_subframe1_label6,accountingpage_subframe1_label8],list_fg=text_color, targeted_widget=accountingpage_subframe1_label4,targeted_fg=sub_maincolor, targeted_frame=accountingpage_subframe2_frame3, frame_list=page_list))

    accountingpage_subframe1_label5 = Label(accountingpage_subframe1,text=' Budgets',background=light_dark,compound='left',font=('monogram',24),fg=text_color, image = budget_photo)
    accountingpage_subframe1_label5.grid(row=4, column=1, sticky='nsw',pady=(0,20))
    accountingpage_subframe1_label5.bind('<Enter>',lambda event :accountingpage_subframe1_label5.configure(font=(custom_font, 24, 'bold')))
    accountingpage_subframe1_label5.bind('<Leave>',lambda event :accountingpage_subframe1_label5.configure(font=(custom_font, 24)))
    accountingpage_subframe1_label5.bind ('<Button-1>', lambda event : accountingpage_leftside_button_function(widget_list = [accountingpage_subframe1_label2,accountingpage_subframe1_label3,accountingpage_subframe1_label4,accountingpage_subframe1_label5,accountingpage_subframe1_label6,accountingpage_subframe1_label8],list_fg=text_color, targeted_widget=accountingpage_subframe1_label5,targeted_fg=sub_maincolor, targeted_frame=accountingpage_subframe2_frame4, frame_list=page_list))

    accountingpage_subframe1_label6 = Label(accountingpage_subframe1,text=' ChatGPT',background=light_dark,compound='left',font=('monogram',24),fg=text_color, image = chatgpt_photo)
    accountingpage_subframe1_label6.grid(row=5, column=1, sticky='nsw',pady=(0,20))
    accountingpage_subframe1_label6.bind('<Enter>',lambda event :accountingpage_subframe1_label6.configure(font=(custom_font, 24, 'bold')))
    accountingpage_subframe1_label6.bind('<Leave>',lambda event :accountingpage_subframe1_label6.configure(font=(custom_font, 24)))
    accountingpage_subframe1_label6.bind ('<Button-1>', lambda event : accountingpage_leftside_button_function(widget_list = [accountingpage_subframe1_label2,accountingpage_subframe1_label3,accountingpage_subframe1_label4,accountingpage_subframe1_label5,accountingpage_subframe1_label6,accountingpage_subframe1_label8],list_fg=text_color, targeted_widget=accountingpage_subframe1_label6,targeted_fg=sub_maincolor, targeted_frame=accountingpage_subframe2_frame5, frame_list=page_list))

    #Minor button
    accountingpage_subframe1_label7 = Label(accountingpage_subframe1,text='MINOR',background=light_dark,compound='left',font=('monogram',24),fg=sub_textcolor)
    accountingpage_subframe1_label7.grid(row=6, column=1, sticky='nsw',pady=(0,20))

    accountingpage_subframe1_label8 = Label(accountingpage_subframe1,text=' Settings',background=light_dark,compound='left',font=('monogram',24),fg=text_color, image = setting_photo)
    accountingpage_subframe1_label8.grid(row=7, column=1, sticky='nsw',pady=(0,20))
    accountingpage_subframe1_label8.bind('<Enter>',lambda event :accountingpage_subframe1_label8.configure(font=(custom_font, 24, 'bold')))
    accountingpage_subframe1_label8.bind('<Leave>',lambda event :accountingpage_subframe1_label8.configure(font=(custom_font, 24)))
    accountingpage_subframe1_label8.bind ('<Button-1>', lambda event : accountingpage_leftside_button_function(widget_list = [accountingpage_subframe1_label2,accountingpage_subframe1_label3,accountingpage_subframe1_label4,accountingpage_subframe1_label5,accountingpage_subframe1_label6,accountingpage_subframe1_label8],list_fg=text_color, targeted_widget=accountingpage_subframe1_label8,targeted_fg=sub_maincolor, targeted_frame=accountingpage_subframe2_frame6, frame_list=page_list))


    #page startup thing so the user see the dashboard as a default
    accountingpage_leftside_button_function(widget_list = [accountingpage_subframe1_label2,accountingpage_subframe1_label3,accountingpage_subframe1_label4,accountingpage_subframe1_label5,accountingpage_subframe1_label6,accountingpage_subframe1_label8],list_fg=text_color, targeted_widget=accountingpage_subframe1_label2,targeted_fg=sub_maincolor, targeted_frame=accountingpage_subframe2_frame1, frame_list=page_list)
def build_accounting_page_transaction(master,call=False):
    def set_custom_combobox_value(widget,error_msg_widget,fetched_widget,setup):
        if not setup:
            widget.set('')
        value = fetched_widget.get()
        if len(value) > 1:
            placed_value = api.offline_fetch_account_from_type(value)
            widget.configure(values=placed_value)
    def set_combobox_account_type(widget,error_msg_widget,fetched_widget,setup):
        if not setup:
            widget.set('')
        try:
            fetched_value = fetched_widget.get()
            value = account_formula[fetched_value]['access_list']
            widget.configure(values=value)
        except Exception as e:
            error_msg_widget.configure(text=str(e))

    def back_button():
        accountingpage_subframe2_frame2_buttonpage.grid_forget()
        accountingpage_subframe2_frame2_infopage_frame2.grid_forget()
        accountingpage_subframe2_frame2_infopage_dataframe.grid(column=0,row=0,sticky='nsew')
        reset()
    def reset():
        accountingpage_subframe2_frame2_buttonpage_labelframe1_entry1.configure(state='readonly')
        accountingpage_subframe2_frame2_buttonpage_labelframe1_entry2.configure(state='readonly')
        accountingpage_subframe2_frame2_buttonpage_labelframe2_entry1.configure(state='readonly')
        accountingpage_subframe2_frame2_buttonpage_labelframe2_entry2.configure(state='readonly')
        accountingpage_subframe2_frame2_buttonpage_labelframe3_frame1_combobox1.configure(state='readonly',values=[])
        accountingpage_subframe2_frame2_buttonpage_labelframe3_frame1_combobox2.configure(state='readonly',values=[])
        accountingpage_subframe2_frame2_buttonpage_labelframe3_frame1_combobox3.configure(state='readonly')
        accountingpage_subframe2_frame2_buttonpage_labelframe3_entry2.configure(state='normal')
        accountingpage_subframe2_frame2_buttonpage_labelframe3_entry3.configure(state='normal')

        accountingpage_subframe2_frame2_buttonpage_labelframe1_entry1.set('')
        accountingpage_subframe2_frame2_buttonpage_labelframe1_entry2.set('')
        accountingpage_subframe2_frame2_buttonpage_labelframe2_entry1.set('')
        accountingpage_subframe2_frame2_buttonpage_labelframe2_entry2.set('')
        accountingpage_subframe2_frame2_buttonpage_labelframe3_frame1_combobox1.set('')
        accountingpage_subframe2_frame2_buttonpage_labelframe3_frame1_combobox2.set('')
        accountingpage_subframe2_frame2_buttonpage_labelframe3_frame1_combobox3.set('')
        accountingpage_subframe2_frame2_buttonpage_labelframe3_entry2.delete(0,END)
        accountingpage_subframe2_frame2_buttonpage_labelframe3_entry2.insert(0,'\u200BEnter here')
        accountingpage_subframe2_frame2_buttonpage_labelframe3_entry3.delete(0,END)
        accountingpage_subframe2_frame2_buttonpage_labelframe3_entry3.insert(0,'\u200Beg.1000')
        accountingpage_subframe2_frame2_buttonpage_labelframe3_entry2.configure(fg=sub_textcolor)
        accountingpage_subframe2_frame2_buttonpage_labelframe3_entry3.configure(fg=sub_textcolor)
        accountingpage_subframe2_frame2_treeview.unbind('<<TreeviewSelect>>')
        accountingpage_subframe2_frame2_buttonpage_labelframe1_entry1.configure(values=[])
        accountingpage_subframe2_frame2_buttonpage_labelframe1_entry1.unbind('<<ComboboxSelected>>')
        accountingpage_subframe2_frame2_buttonpage_labelframe1_entry2.configure(values=[])
        accountingpage_subframe2_frame2_buttonpage_labelframe2_entry1.unbind('<<ComboboxSelected>>')
        accountingpage_subframe2_frame2_buttonpage_labelframe2_entry1.configure(values=[])
        accountingpage_subframe2_frame2_buttonpage_labelframe2_entry2.configure(values=[])

    def to_button_page(type_of_command = str in ['add','remove','edit','search']): 
        def treeview_select(event,lock=bool):
            value = accountingpage_subframe2_frame2_treeview.focus()
            state.treeview_selected_row = value
            if value:
                accountingpage_subframe2_frame2_treeview.unbind('<<TreeviewSelect>>')
                accountingpage_subframe2_frame2_buttonpage_labelframe1_entry1.configure(state='readonly')
                accountingpage_subframe2_frame2_buttonpage_labelframe1_entry2.configure(state='readonly')
                accountingpage_subframe2_frame2_buttonpage_labelframe2_entry1.configure(state='readonly')
                accountingpage_subframe2_frame2_buttonpage_labelframe2_entry2.configure(state='readonly')
                accountingpage_subframe2_frame2_buttonpage_labelframe3_frame1_combobox1.configure(state='readonly')
                accountingpage_subframe2_frame2_buttonpage_labelframe3_frame1_combobox2.configure(state='readonly')
                accountingpage_subframe2_frame2_buttonpage_labelframe3_frame1_combobox3.configure(state='readonly')
                accountingpage_subframe2_frame2_buttonpage_labelframe3_entry2.configure(state='normal',fg=text_color)
                accountingpage_subframe2_frame2_buttonpage_labelframe3_entry3.configure(state='normal',fg=text_color)
                accountingpage_subframe2_frame2_infopage_frame2.grid_forget()
                accountingpage_subframe2_frame2_infopage_dataframe.grid_forget()
                accountingpage_subframe2_frame2_buttonpage.grid(column=0,row=0,sticky='nsew')

                treeview_values = accountingpage_subframe2_frame2_treeview.item(value,'values')
                accountingpage_subframe2_frame2_buttonpage_labelframe1_entry1.set(treeview_values[1])
                accountingpage_subframe2_frame2_buttonpage_labelframe1_entry2.set(treeview_values[2])
                accountingpage_subframe2_frame2_buttonpage_labelframe2_entry1.set(treeview_values[3])
                accountingpage_subframe2_frame2_buttonpage_labelframe2_entry2.set(treeview_values[4])
                date = treeview_values[5].split('-')
                accountingpage_subframe2_frame2_buttonpage_labelframe3_frame1_combobox1.set(date[0])
                accountingpage_subframe2_frame2_buttonpage_labelframe3_frame1_combobox2.set(date[1])
                accountingpage_subframe2_frame2_buttonpage_labelframe3_frame1_combobox3.set(date[2])
                accountingpage_subframe2_frame2_buttonpage_labelframe3_entry2.delete(0,END)
                accountingpage_subframe2_frame2_buttonpage_labelframe3_entry2.insert(0,treeview_values[6])
                accountingpage_subframe2_frame2_buttonpage_labelframe3_entry3.delete(0,END)
                accountingpage_subframe2_frame2_buttonpage_labelframe3_entry3.insert(0,treeview_values[7])
                state.treeview_id = treeview_values[0]


                set_custom_combobox_value(accountingpage_subframe2_frame2_buttonpage_labelframe1_entry2,accountingpage_subframe2_frame2_messages_label1,accountingpage_subframe2_frame2_buttonpage_labelframe1_entry1,True)
                set_combobox_account_type(accountingpage_subframe2_frame2_buttonpage_labelframe2_entry1,accountingpage_subframe2_frame2_messages_label1,accountingpage_subframe2_frame2_buttonpage_labelframe1_entry1,True)
                set_custom_combobox_value(accountingpage_subframe2_frame2_buttonpage_labelframe2_entry2,accountingpage_subframe2_frame2_messages_label1,accountingpage_subframe2_frame2_buttonpage_labelframe2_entry1,True)

                if lock:
                    accountingpage_subframe2_frame2_buttonpage_labelframe1_entry1.configure(state='disabled')
                    accountingpage_subframe2_frame2_buttonpage_labelframe1_entry2.configure(state='disabled')
                    accountingpage_subframe2_frame2_buttonpage_labelframe2_entry1.configure(state='disabled')
                    accountingpage_subframe2_frame2_buttonpage_labelframe2_entry2.configure(state='disabled')
                    accountingpage_subframe2_frame2_buttonpage_labelframe3_frame1_combobox1.configure(state='disabled')
                    accountingpage_subframe2_frame2_buttonpage_labelframe3_frame1_combobox2.configure(state='disabled')
                    accountingpage_subframe2_frame2_buttonpage_labelframe3_frame1_combobox3.configure(state='disabled')
                    accountingpage_subframe2_frame2_buttonpage_labelframe3_entry2.configure(state='disabled')
                    accountingpage_subframe2_frame2_buttonpage_labelframe3_entry3.configure(state='disabled')
        if getattr(state,'is_online') == False:
            if type_of_command == 'add':
                reset()
                accountingpage_subframe2_frame2_infopage_frame2.grid_forget()
                accountingpage_subframe2_frame2_infopage_dataframe.grid_forget()
                accountingpage_subframe2_frame2_buttonpage.grid(column=0,row=0,sticky='nsew')
                accountingpage_subframe2_frame2_buttonpage_labelframe4_label1.configure(text = ' - Choose the Type in the From First')
                accountingpage_subframe2_frame2_buttonpage_labelframe4_label2.configure(text = ' - Date format is DD-MM-YY')
                accountingpage_subframe2_frame2_buttonpage_frame1_button1.configure(command=back_button)

                accountingpage_subframe2_frame2_buttonpage_labelframe1_entry1.configure(values = [item for item in state.account_type if item != 'expenses'])
                accountingpage_subframe2_frame2_buttonpage_labelframe1_entry1.bind('<<ComboboxSelected>>', lambda event: [set_custom_combobox_value(accountingpage_subframe2_frame2_buttonpage_labelframe1_entry2,accountingpage_subframe2_frame2_messages_label1,accountingpage_subframe2_frame2_buttonpage_labelframe1_entry1,False),set_combobox_account_type(accountingpage_subframe2_frame2_buttonpage_labelframe2_entry1,accountingpage_subframe2_frame2_messages_label1,accountingpage_subframe2_frame2_buttonpage_labelframe1_entry1,False), accountingpage_subframe2_frame2_buttonpage_labelframe2_entry2.set('')])
                accountingpage_subframe2_frame2_buttonpage_labelframe2_entry1.bind('<<ComboboxSelected>>', lambda event: set_custom_combobox_value(accountingpage_subframe2_frame2_buttonpage_labelframe2_entry2,accountingpage_subframe2_frame2_messages_label1,accountingpage_subframe2_frame2_buttonpage_labelframe2_entry1,False) )

                accountingpage_subframe2_frame2_buttonpage_frame1_button2.configure(command = lambda: button_page_command('add'),text='Add')

            elif type_of_command == 'remove':
                reset()
                accountingpage_subframe2_frame2_infopage_frame2.grid(column=0,row=0,sticky='nsew')
                accountingpage_subframe2_frame2_infopage_dataframe.grid_forget()
                accountingpage_subframe2_frame2_buttonpage.grid_forget()
                accountingpage_subframe2_frame2_buttonpage_labelframe4_label1.configure(text = ' - You cant Edit the entry boxes')
                accountingpage_subframe2_frame2_buttonpage_labelframe4_label2.configure(text = ' - Click back if u want to change')

                accountingpage_subframe2_frame2_buttonpage_frame1_button1.configure(command=lambda:to_button_page('remove'))
                accountingpage_subframe2_frame2_treeview.bind('<<TreeviewSelect>>',lambda event: treeview_select(event=event,lock=True))
                accountingpage_subframe2_frame2_buttonpage_frame1_button2.configure(command = lambda: button_page_command('remove'),text='Remove')

            elif type_of_command == 'edit':
                reset()
                accountingpage_subframe2_frame2_infopage_frame2.grid(column=0,row=0,sticky='nsew')
                accountingpage_subframe2_frame2_infopage_dataframe.grid_forget()
                accountingpage_subframe2_frame2_buttonpage.grid_forget()
                accountingpage_subframe2_frame2_buttonpage_labelframe4_label1.configure(text = ' - Click back if u want to change')
                accountingpage_subframe2_frame2_buttonpage_labelframe4_label2.configure(text = ' - Confirm after editing')

                accountingpage_subframe2_frame2_buttonpage_labelframe1_entry1.configure(values = [item for item in state.account_type if item != 'expenses'])
                accountingpage_subframe2_frame2_buttonpage_labelframe1_entry1.bind('<<ComboboxSelected>>', lambda event: [set_custom_combobox_value(accountingpage_subframe2_frame2_buttonpage_labelframe1_entry2,accountingpage_subframe2_frame2_messages_label1,accountingpage_subframe2_frame2_buttonpage_labelframe1_entry1,False),set_combobox_account_type(accountingpage_subframe2_frame2_buttonpage_labelframe2_entry1,accountingpage_subframe2_frame2_messages_label1,accountingpage_subframe2_frame2_buttonpage_labelframe1_entry1,False), accountingpage_subframe2_frame2_buttonpage_labelframe2_entry2.set('')])
                accountingpage_subframe2_frame2_buttonpage_labelframe2_entry1.bind('<<ComboboxSelected>>', lambda event: set_custom_combobox_value(accountingpage_subframe2_frame2_buttonpage_labelframe2_entry2,accountingpage_subframe2_frame2_messages_label1,accountingpage_subframe2_frame2_buttonpage_labelframe2_entry1,False) )
                accountingpage_subframe2_frame2_buttonpage_labelframe2_entry1.configure

                accountingpage_subframe2_frame2_buttonpage_frame1_button1.configure(command=lambda:to_button_page('remove'))
                accountingpage_subframe2_frame2_treeview.bind('<<TreeviewSelect>>',lambda event: treeview_select(event=event,lock=False))
                accountingpage_subframe2_frame2_buttonpage_frame1_button2.configure(command = lambda: button_page_command('edit'),text='Edit')

            elif type_of_command == 'search':
                reset()
                accountingpage_subframe2_frame2_infopage_frame2.grid_forget()
                accountingpage_subframe2_frame2_infopage_dataframe.grid_forget()
                accountingpage_subframe2_frame2_buttonpage.grid(column=0,row=0,sticky='nsew')
                accountingpage_subframe2_frame2_buttonpage_labelframe4_label1.configure(text = ' - Enter a keyword to locate entries')
                accountingpage_subframe2_frame2_buttonpage_labelframe4_label2.configure(text = ' - For date month search do 00-02-0000')
                
                accountingpage_subframe2_frame2_buttonpage_labelframe1_entry1.bind('<<ComboboxSelected>>', lambda event: set_custom_combobox_value(accountingpage_subframe2_frame2_buttonpage_labelframe1_entry2,accountingpage_subframe2_frame2_messages_label1,accountingpage_subframe2_frame2_buttonpage_labelframe1_entry1,False))
                accountingpage_subframe2_frame2_buttonpage_labelframe1_entry1.configure(values = [*[''],*[item for item in state.account_type if item != 'expenses']])
                accountingpage_subframe2_frame2_buttonpage_labelframe2_entry1.bind('<<ComboboxSelected>>', lambda event: set_custom_combobox_value(accountingpage_subframe2_frame2_buttonpage_labelframe2_entry2,accountingpage_subframe2_frame2_messages_label1,accountingpage_subframe2_frame2_buttonpage_labelframe2_entry1,False))
                accountingpage_subframe2_frame2_buttonpage_labelframe2_entry1.configure(values=[*[''],*state.account_type])

                accountingpage_subframe2_frame2_buttonpage_frame1_button1.configure(command=back_button)
                accountingpage_subframe2_frame2_buttonpage_frame1_button2.configure(command = lambda: button_page_command('search'),text='Search')
    def button_page_command(type_of_command = str ):
        if getattr(state,'is_online') == False:
            if type_of_command == 'add':
                dates = f'{accountingpage_subframe2_frame2_buttonpage_labelframe3_frame1_combobox1.get()}-{accountingpage_subframe2_frame2_buttonpage_labelframe3_frame1_combobox2.get()}-{accountingpage_subframe2_frame2_buttonpage_labelframe3_frame1_combobox3.get()}'
                is_success, data = api.offline_add_entry(accountingpage_subframe2_frame2_buttonpage_labelframe1_entry1,accountingpage_subframe2_frame2_buttonpage_labelframe1_entry2,accountingpage_subframe2_frame2_buttonpage_labelframe2_entry1,accountingpage_subframe2_frame2_buttonpage_labelframe2_entry2,accountingpage_subframe2_frame2_messages_label1,dates,accountingpage_subframe2_frame2_buttonpage_labelframe3_entry3,accountingpage_subframe2_frame2_buttonpage_labelframe3_entry2)
                if is_success:
                    accountingpage_subframe2_frame2_treeview.insert('','end',values=data)
                    try:
                        num = float(accountingpage_subframe2_frame2_infopage_label3.cget('text')) + float(accountingpage_subframe2_frame2_buttonpage_labelframe3_entry3.get())
                        accountingpage_subframe2_frame2_infopage_label3.configure(text=str(num))
                        count = int(accountingpage_subframe2_frame2_infopage_label5.cget('text')) + 1
                        accountingpage_subframe2_frame2_infopage_label5.configure(text=str(count))
                    except Exception as e:
                        print(str(e))
                    to_button_page('add')

            if type_of_command == 'remove':
                is_success = api.offline_remove_entry(error_msg_widget=accountingpage_subframe2_frame2_messages_label1,ids=int(state.treeview_id))
                if is_success:
                    accountingpage_subframe2_frame2_treeview.delete(state.treeview_selected_row)
                    try:
                        num = float(accountingpage_subframe2_frame2_infopage_label3.cget('text')) - float(accountingpage_subframe2_frame2_buttonpage_labelframe3_entry3.get())
                        accountingpage_subframe2_frame2_infopage_label3.configure(text=str(num))
                        count = int(accountingpage_subframe2_frame2_infopage_label5.cget('text')) - 1
                        accountingpage_subframe2_frame2_infopage_label5.configure(text=str(count))
                    except Exception as e:
                        print(str(e))
                    to_button_page('remove')

            if type_of_command == 'edit':
                dates = f'{accountingpage_subframe2_frame2_buttonpage_labelframe3_frame1_combobox1.get()}-{accountingpage_subframe2_frame2_buttonpage_labelframe3_frame1_combobox2.get()}-{accountingpage_subframe2_frame2_buttonpage_labelframe3_frame1_combobox3.get()}'
                is_success, data = api.offline_edit_entry(state.treeview_id,accountingpage_subframe2_frame2_buttonpage_labelframe1_entry1,accountingpage_subframe2_frame2_buttonpage_labelframe1_entry2,accountingpage_subframe2_frame2_buttonpage_labelframe2_entry1,accountingpage_subframe2_frame2_buttonpage_labelframe2_entry2,accountingpage_subframe2_frame2_messages_label1,dates,accountingpage_subframe2_frame2_buttonpage_labelframe3_entry3,accountingpage_subframe2_frame2_buttonpage_labelframe3_entry2,search_return_list=True)
                if is_success:
                    value = accountingpage_subframe2_frame2_treeview.item(state.treeview_selected_row,'values')
                    try:
                        num = float(accountingpage_subframe2_frame2_infopage_label3.cget('text')) - float(value[8]) + float(accountingpage_subframe2_frame2_buttonpage_labelframe3_entry3.get())
                        accountingpage_subframe2_frame2_infopage_label3.configure(text=str(num))
                    except Exception as e:
                        print(str(e))

                    accountingpage_subframe2_frame2_treeview.item(state.treeview_selected_row,values=data)
                    to_button_page('edit')

            if type_of_command == 'search':
                
    def calculate_dataframe(setup=False):
        index = 10 if setup else 8
        total = 0.0

        for i in accountingpage_subframe2_frame2_treeview.get_children():
            vals = accountingpage_subframe2_frame2_treeview.item(i, "values")
            if len(vals) > 7:
                total += float(vals[index])

        accountingpage_subframe2_frame2_infopage_label3.configure(text=str(total))
        accountingpage_subframe2_frame2_infopage_label5.configure(text=str(len(accountingpage_subframe2_frame2_treeview.get_children())))

    accountingpage_subframe2_frame2_transactionpage = Frame(master, background=sub_lightdark)
    accountingpage_subframe2_frame2_transactionpage.grid(column=0,row=0,sticky='nsew')

    accountingpage_subframe2_frame2_scrollbar = ttk.Scrollbar(accountingpage_subframe2_frame2_transactionpage)
    accountingpage_subframe2_frame2_scrollbar.pack(side='right',fill='y',pady=(0,5))

    headings = ('ID','From','From2','To','To2','Date','Description','Amount')
    accountingpage_subframe2_frame2_treeview = ttk.Treeview(accountingpage_subframe2_frame2_transactionpage,columns=headings, show='headings',yscrollcommand=accountingpage_subframe2_frame2_scrollbar,selectmode='browse')
    accountingpage_subframe2_frame2_scrollbar.configure(command=accountingpage_subframe2_frame2_treeview.yview)

    accountingpage_subframe2_frame2_treeview.column('ID',anchor='w',stretch=True,minwidth=30,width=30)
    accountingpage_subframe2_frame2_treeview.heading('ID', text = 'ID')

    accountingpage_subframe2_frame2_treeview.column('From',anchor='w',stretch=True,minwidth=50,width=100)
    accountingpage_subframe2_frame2_treeview.heading('From', text = 'From')

    accountingpage_subframe2_frame2_treeview.column('From2',anchor='w',stretch=True,minwidth=50,width=100)
    accountingpage_subframe2_frame2_treeview.heading('From2', text = '    ')

    accountingpage_subframe2_frame2_treeview.column('To',anchor='w',stretch=True,minwidth=50,width=100)
    accountingpage_subframe2_frame2_treeview.heading('To', text = 'To')

    accountingpage_subframe2_frame2_treeview.column('To2',anchor='w',stretch=True,minwidth=50,width=100)
    accountingpage_subframe2_frame2_treeview.heading('To2', text = '    ')

    accountingpage_subframe2_frame2_treeview.column('Date',anchor='w',stretch=True,minwidth=50,width=100)
    accountingpage_subframe2_frame2_treeview.heading('Date', text = 'Date')

    accountingpage_subframe2_frame2_treeview.column('Description',anchor='w',stretch=True,minwidth=50,width=120)
    accountingpage_subframe2_frame2_treeview.heading('Description', text = 'Description')

    accountingpage_subframe2_frame2_treeview.column('Amount',anchor='w',stretch=True,minwidth=50,width=100)
    accountingpage_subframe2_frame2_treeview.heading('Amount', text = 'Amount')

    accountingpage_subframe2_frame2_treeview.pack(side='top',fill='both', expand=True,pady=(0,5))


    #Server messages
    accountingpage_subframe2_frame2_messages_border = Frame(master, background=light_dark)
    accountingpage_subframe2_frame2_messages_border.grid(column=0,row=1,sticky='nsew')

    accountingpage_subframe2_frame2_messages = Frame(accountingpage_subframe2_frame2_messages_border, background=sub_lightdark)
    accountingpage_subframe2_frame2_messages.pack(side='top',fill='both', expand=True,pady=(3,0),padx=3)

    accountingpage_subframe2_frame2_messages_label1 = Label(accountingpage_subframe2_frame2_messages, text='', background=sub_lightdark, fg=error_color,font=('monogram',20))
    accountingpage_subframe2_frame2_messages_label1.grid(column=0,row=0,sticky='nsw')


    #Bottom section
    accountingpage_subframe2_frame2_infopage_border = Frame(master, background=light_dark)
    accountingpage_subframe2_frame2_infopage_border.grid(column=0,row=2,sticky='nsew',pady=(0,3))

    accountingpage_subframe2_frame2_infopage = Frame(accountingpage_subframe2_frame2_infopage_border, background=sub_lightdark)
    accountingpage_subframe2_frame2_infopage.pack(side='top',fill='both', expand=True,pady=(3,0),padx=3)
    accountingpage_subframe2_frame2_infopage.grid_columnconfigure(0,weight=2)
    accountingpage_subframe2_frame2_infopage.grid_columnconfigure(1,weight=0)
    accountingpage_subframe2_frame2_infopage.grid_rowconfigure(0,weight=1)

    accountingpage_subframe2_frame2_infopage_leftframe = Frame(accountingpage_subframe2_frame2_infopage, background=sub_lightdark,height=310,width=700)
    accountingpage_subframe2_frame2_infopage_leftframe.grid_propagate(False)
    accountingpage_subframe2_frame2_infopage_leftframe.grid_columnconfigure(0,weight=1)
    accountingpage_subframe2_frame2_infopage_leftframe.grid_rowconfigure(0,weight=1)
    accountingpage_subframe2_frame2_infopage_leftframe.grid(column=0,row=0,sticky='nsew')

    accountingpage_subframe2_frame2_infopage_dataframe = Frame(accountingpage_subframe2_frame2_infopage_leftframe, background=sub_lightdark,height=310,width=700)
    accountingpage_subframe2_frame2_infopage_dataframe.grid_propagate(False)
    accountingpage_subframe2_frame2_infopage_dataframe.grid(column=0,row=0,sticky='nsew')
    accountingpage_subframe2_frame2_infopage_dataframe.grid_columnconfigure([0,1],weight=1)
    accountingpage_subframe2_frame2_infopage_dataframe.grid_rowconfigure(0,weight=1)

    accountingpage_subframe2_frame2_infopage_labelframe2 = LabelFrame(accountingpage_subframe2_frame2_infopage_dataframe,text='Table Data',background=sub_lightdark,font=(custom_font,20,'bold'),fg=text_color)
    accountingpage_subframe2_frame2_infopage_labelframe2.grid(column=0,row=0,sticky='nsew',pady=(0,5),padx=[0,5])

    accountingpage_subframe2_frame2_infopage_label1 = Label(accountingpage_subframe2_frame2_infopage_labelframe2, text='Date', background=sub_lightdark, fg=text_color,font=('monogram',20))
    accountingpage_subframe2_frame2_infopage_label1.grid(column=0,row=0,sticky='nsw',pady=5,padx=[3,0])
    accountingpage_subframe2_frame2_infopage_equal1 = Label(accountingpage_subframe2_frame2_infopage_labelframe2, text=':', background=sub_lightdark, fg=text_color,font=('monogram',20))
    accountingpage_subframe2_frame2_infopage_equal1.grid(column=1,row=0,sticky='nsew',pady=5)
    accountingpage_subframe2_frame2_infopage_label1s = Label(accountingpage_subframe2_frame2_infopage_labelframe2, text='00-00-0000', background=sub_lightdark, fg=text_color,font=('monogram',20))
    accountingpage_subframe2_frame2_infopage_label1s.grid(column=2,row=0,sticky='nsw',pady=5,padx=[3,0])

    accountingpage_subframe2_frame2_infopage_label2 = Label(accountingpage_subframe2_frame2_infopage_labelframe2, text='Total Amount Displayed', background=sub_lightdark, fg=text_color,font=('monogram',20))
    accountingpage_subframe2_frame2_infopage_label2.grid(column=0,row=1,sticky='nsw',pady=(0,5),padx=[3,0])
    accountingpage_subframe2_frame2_infopage_equal2 = Label(accountingpage_subframe2_frame2_infopage_labelframe2, text=':', background=sub_lightdark, fg=text_color,font=('monogram',20))
    accountingpage_subframe2_frame2_infopage_equal2.grid(column=1,row=1,sticky='nsew',pady=5)
    accountingpage_subframe2_frame2_infopage_label3 = Label(accountingpage_subframe2_frame2_infopage_labelframe2, text='0', background=sub_lightdark, fg=text_color,font=('monogram',20,'bold'))
    accountingpage_subframe2_frame2_infopage_label3.grid(column=2,row=1,sticky='nsw',pady=(0,5))    
    
    accountingpage_subframe2_frame2_infopage_label4 = Label(accountingpage_subframe2_frame2_infopage_labelframe2, text='Total Row Displayed', background=sub_lightdark, fg=text_color,font=('monogram',20))
    accountingpage_subframe2_frame2_infopage_label4.grid(column=0,row=2,sticky='nsw',pady=(0,5),padx=[3,0])
    accountingpage_subframe2_frame2_infopage_equal3 = Label(accountingpage_subframe2_frame2_infopage_labelframe2, text=':', background=sub_lightdark, fg=text_color,font=('monogram',20))
    accountingpage_subframe2_frame2_infopage_equal3.grid(column=1,row=2,sticky='nsew',pady=5)
    accountingpage_subframe2_frame2_infopage_label5 = Label(accountingpage_subframe2_frame2_infopage_labelframe2, text='0', background=sub_lightdark, fg=text_color,font=('monogram',20,'bold'))
    accountingpage_subframe2_frame2_infopage_label5.grid(column=2,row=2,sticky='nsw',pady=(0,5))    

    accountingpage_subframe2_frame2_infopage_labelframe1 = LabelFrame(accountingpage_subframe2_frame2_infopage_dataframe,text='Explanation',background=sub_lightdark,font=(custom_font,20,'bold'),fg=text_color)
    accountingpage_subframe2_frame2_infopage_labelframe1.grid(column=1,row=0,sticky='nsew',pady=(0,5),padx=[0,5])

    accountingpage_subframe2_frame2_infopage_labelframe1_label1 = Label(accountingpage_subframe2_frame2_infopage_labelframe1, text=' - Use Date or Search to show Transaction Logs', background=sub_lightdark, fg=text_color,font=('monogram',20))
    accountingpage_subframe2_frame2_infopage_labelframe1_label1.pack(side='top',anchor='w',pady=[0,5])

    accountingpage_subframe2_frame2_infopage_labelframe1_label1 = Label(accountingpage_subframe2_frame2_infopage_labelframe1, text=' - Account is tied to transactions', background=sub_lightdark, fg=text_color,font=('monogram',20))
    accountingpage_subframe2_frame2_infopage_labelframe1_label1.pack(side='top',anchor='w',pady=[0,5])

    accountingpage_subframe2_frame2_infopage_labelframe1_label1 = Label(accountingpage_subframe2_frame2_infopage_labelframe1, text=' - Further help is at the README file ', background=sub_lightdark, fg=text_color,font=('monogram',20))
    accountingpage_subframe2_frame2_infopage_labelframe1_label1.pack(side='top',anchor='w',pady=[0,5])
    Label(accountingpage_subframe2_frame2_infopage_labelframe1, text=' - IT is NOT recomended to have\n   Transaction row > 10000 on display', background=sub_lightdark, fg=text_color,font=('monogram',20),justify='left').pack(side='top',anchor='w',pady=[0,5])

    #Add / remove/ edit page
    #The Label to make the user pick got remove / edit
    accountingpage_subframe2_frame2_infopage_frame2 = Frame(accountingpage_subframe2_frame2_infopage_leftframe,background=light_dark)
    accountingpage_subframe2_frame2_infopage_frame2.grid_columnconfigure(0,weight=1)
    accountingpage_subframe2_frame2_infopage_frame2.grid_rowconfigure(0,weight=1)
    accountingpage_subframe2_frame2_infopage_frame2_label1 = Label(accountingpage_subframe2_frame2_infopage_frame2, text='Please click on the row\n you want to change', background=sub_lightdark, fg=text_color,font=('monogram',20))
    accountingpage_subframe2_frame2_infopage_frame2_label1.grid(column=0,row=0,sticky='nsew')
    accountingpage_subframe2_frame2_infopage_frame2_button1 = Button(accountingpage_subframe2_frame2_infopage_frame2,text='Back',foreground=text_color,background=light_dark,font=(custom_font,20,'bold'),command=back_button)
    accountingpage_subframe2_frame2_infopage_frame2_button1.grid(column=0,row=1,sticky='nsew',pady=[3,0])

    #Foundation Frame
    accountingpage_subframe2_frame2_buttonpage = Frame(accountingpage_subframe2_frame2_infopage_leftframe, background=sub_lightdark,height=310,width=700)
    accountingpage_subframe2_frame2_buttonpage.grid_propagate(False)
    accountingpage_subframe2_frame2_buttonpage.grid_rowconfigure([0,1],weight=1)
    accountingpage_subframe2_frame2_buttonpage.grid_columnconfigure([0,1],weight=1,uniform='a')


    #Label Frame for FROM
    accountingpage_subframe2_frame2_buttonpage_labelframe1 = LabelFrame(accountingpage_subframe2_frame2_buttonpage, text='From', background=sub_lightdark, fg=text_color,font=('monogram',20,'bold'))
    accountingpage_subframe2_frame2_buttonpage_labelframe1.grid(column=0,row=0,sticky='nsew',padx=[5,0])
    accountingpage_subframe2_frame2_buttonpage_labelframe1.grid_rowconfigure([0,1],weight=1)
    accountingpage_subframe2_frame2_buttonpage_labelframe1.grid_columnconfigure(2,weight=1)

    accountingpage_subframe2_frame2_buttonpage_labelframe1_label1 = Label(accountingpage_subframe2_frame2_buttonpage_labelframe1, text='Type', background=sub_lightdark, fg=text_color,font=('monogram',20))
    accountingpage_subframe2_frame2_buttonpage_labelframe1_label1.grid(column=0,row=0,sticky='nw',pady=5)
    accountingpage_subframe2_frame2_buttonpage_labelframe1_equal1 = Label(accountingpage_subframe2_frame2_buttonpage_labelframe1, text=':', background=sub_lightdark, fg=text_color,font=('monogram',20))
    accountingpage_subframe2_frame2_buttonpage_labelframe1_equal1.grid(column=1,row=0,sticky='nw',pady=5)
    accountingpage_subframe2_frame2_buttonpage_labelframe1_entry1 = ttk.Combobox(accountingpage_subframe2_frame2_buttonpage_labelframe1, background = light_dark, foreground = text_color,font=('monogram',20),state='readonly',justify='left')
    accountingpage_subframe2_frame2_buttonpage_labelframe1_entry1.grid(column=2,row=0,sticky='new',pady=5,padx=[0,5])

    accountingpage_subframe2_frame2_buttonpage_labelframe1_label2 = Label(accountingpage_subframe2_frame2_buttonpage_labelframe1, text='Account   ', background=sub_lightdark, fg=text_color,font=('monogram',20))
    accountingpage_subframe2_frame2_buttonpage_labelframe1_label2.grid(column=0,row=1,sticky='nw',pady=5)
    accountingpage_subframe2_frame2_buttonpage_labelframe1_equal2 = Label(accountingpage_subframe2_frame2_buttonpage_labelframe1, text=':', background=sub_lightdark, fg=text_color,font=('monogram',20))
    accountingpage_subframe2_frame2_buttonpage_labelframe1_equal2.grid(column=1,row=1,sticky='nw',pady=5)
    accountingpage_subframe2_frame2_buttonpage_labelframe1_entry2 = ttk.Combobox(accountingpage_subframe2_frame2_buttonpage_labelframe1, background = light_dark, foreground = text_color,font=('monogram',20),state='readonly')
    accountingpage_subframe2_frame2_buttonpage_labelframe1_entry2.grid(column=2,row=1,sticky='new',pady=5,padx=[0,5])

    #Label Frame for TO
    accountingpage_subframe2_frame2_buttonpage_labelframe2 = LabelFrame(accountingpage_subframe2_frame2_buttonpage, text='To', background=sub_lightdark, fg=text_color,font=('monogram',20,'bold'))
    accountingpage_subframe2_frame2_buttonpage_labelframe2.grid(column=0,row=1,sticky='nsew',padx=[5,0])
    accountingpage_subframe2_frame2_buttonpage_labelframe2.grid_rowconfigure([0,1],weight=1)
    accountingpage_subframe2_frame2_buttonpage_labelframe2.grid_columnconfigure(2,weight=1)

    accountingpage_subframe2_frame2_buttonpage_labelframe2_label1 = Label(accountingpage_subframe2_frame2_buttonpage_labelframe2, text='Type', background=sub_lightdark, fg=text_color,font=('monogram',20))
    accountingpage_subframe2_frame2_buttonpage_labelframe2_label1.grid(column=0,row=0,sticky='nw',pady=5)
    accountingpage_subframe2_frame2_buttonpage_labelframe2_equal1 = Label(accountingpage_subframe2_frame2_buttonpage_labelframe2, text=':', background=sub_lightdark, fg=text_color,font=('monogram',20))
    accountingpage_subframe2_frame2_buttonpage_labelframe2_equal1.grid(column=1,row=0,sticky='nw',pady=5)
    accountingpage_subframe2_frame2_buttonpage_labelframe2_entry1 = ttk.Combobox(accountingpage_subframe2_frame2_buttonpage_labelframe2, background = light_dark, foreground = text_color,font=('monogram',20),state='readonly')
    accountingpage_subframe2_frame2_buttonpage_labelframe2_entry1.grid(column=2,row=0,sticky='new',pady=5,padx=[0,5])

    accountingpage_subframe2_frame2_buttonpage_labelframe2_label2 = Label(accountingpage_subframe2_frame2_buttonpage_labelframe2, text='Account   ', background=sub_lightdark, fg=text_color,font=('monogram',20))
    accountingpage_subframe2_frame2_buttonpage_labelframe2_label2.grid(column=0,row=1,sticky='nw',pady=5)
    accountingpage_subframe2_frame2_buttonpage_labelframe2_equal2 = Label(accountingpage_subframe2_frame2_buttonpage_labelframe2, text=':', background=sub_lightdark, fg=text_color,font=('monogram',20))
    accountingpage_subframe2_frame2_buttonpage_labelframe2_equal2.grid(column=1,row=1,sticky='nw',pady=5)
    accountingpage_subframe2_frame2_buttonpage_labelframe2_entry2 = ttk.Combobox(accountingpage_subframe2_frame2_buttonpage_labelframe2, background = light_dark, foreground = text_color,font=('monogram',20),state='readonly')
    accountingpage_subframe2_frame2_buttonpage_labelframe2_entry2.grid(column=2,row=1,sticky='new',pady=5,padx=[0,5])


    #Label Frame for DATA
    #Frame setup
    accountingpage_subframe2_frame2_buttonpage_frame1 = Frame(accountingpage_subframe2_frame2_buttonpage,background=sub_lightdark)
    accountingpage_subframe2_frame2_buttonpage_frame1.grid(column=1,row=0,sticky='nsew',rowspan=2,padx=[0,5])
    accountingpage_subframe2_frame2_buttonpage_frame1.grid_columnconfigure(0,weight=1)
    accountingpage_subframe2_frame2_buttonpage_frame1.grid_rowconfigure([0,1],weight=1,uniform='a')

    accountingpage_subframe2_frame2_buttonpage_labelframe3 = LabelFrame(accountingpage_subframe2_frame2_buttonpage_frame1, text='Data', background=sub_lightdark, fg=text_color,font=('monogram',20,'bold'))
    accountingpage_subframe2_frame2_buttonpage_labelframe3.grid(column=0,row=0,sticky='nsew',padx=[0,5])
    accountingpage_subframe2_frame2_buttonpage_labelframe3.grid_rowconfigure([0,1,2],weight=1)
    accountingpage_subframe2_frame2_buttonpage_labelframe3.grid_columnconfigure(2,weight=1)

    accountingpage_subframe2_frame2_buttonpage_labelframe3_label1 = Label(accountingpage_subframe2_frame2_buttonpage_labelframe3, text='Date', background=sub_lightdark, fg=text_color,font=('monogram',20))
    accountingpage_subframe2_frame2_buttonpage_labelframe3_label1.grid(column=0,row=0,sticky='nw',pady=5)
    accountingpage_subframe2_frame2_buttonpage_labelframe3_equal1 = Label(accountingpage_subframe2_frame2_buttonpage_labelframe3, text=':', background=sub_lightdark, fg=text_color,font=('monogram',20))
    accountingpage_subframe2_frame2_buttonpage_labelframe3_equal1.grid(column=1,row=0,sticky='nw',pady=5)
    accountingpage_subframe2_frame2_buttonpage_labelframe3_frame1 = Frame(accountingpage_subframe2_frame2_buttonpage_labelframe3,background=sub_lightdark)
    accountingpage_subframe2_frame2_buttonpage_labelframe3_frame1.grid(column=2,row=0,sticky='new',pady=5,padx=[0,5])
    accountingpage_subframe2_frame2_buttonpage_labelframe3_frame1_combobox1 = ttk.Combobox(accountingpage_subframe2_frame2_buttonpage_labelframe3_frame1, background = light_dark, foreground = text_color,font=('monogram',20),state='readonly',justify='left',width=5)
    accountingpage_subframe2_frame2_buttonpage_labelframe3_frame1_combobox1.pack(side='left')
    accountingpage_subframe2_frame2_buttonpage_labelframe3_frame1_combobox2 = ttk.Combobox(accountingpage_subframe2_frame2_buttonpage_labelframe3_frame1, background = light_dark, foreground = text_color,font=('monogram',20),state='readonly',justify='left',width=5)
    accountingpage_subframe2_frame2_buttonpage_labelframe3_frame1_combobox2.pack(side='left',padx=5)
    accountingpage_subframe2_frame2_buttonpage_labelframe3_frame1_combobox3 = ttk.Combobox(accountingpage_subframe2_frame2_buttonpage_labelframe3_frame1, background = light_dark, foreground = text_color,font=('monogram',20),state='readonly',justify='left',width=7)
    accountingpage_subframe2_frame2_buttonpage_labelframe3_frame1_combobox3.pack(side='left')
    combobox_date_set_year(accountingpage_subframe2_frame2_buttonpage_labelframe3_frame1_combobox3)
    accountingpage_subframe2_frame2_buttonpage_labelframe3_frame1_combobox3.bind('<<ComboboxSelected>>', lambda e: [combobox_date(accountingpage_subframe2_frame2_buttonpage_labelframe3_frame1_combobox1,accountingpage_subframe2_frame2_buttonpage_labelframe3_frame1_combobox2,accountingpage_subframe2_frame2_buttonpage_labelframe3_frame1_combobox3,select='year')])
    accountingpage_subframe2_frame2_buttonpage_labelframe3_frame1_combobox2.bind('<<ComboboxSelected>>', lambda e: [combobox_date(accountingpage_subframe2_frame2_buttonpage_labelframe3_frame1_combobox1,accountingpage_subframe2_frame2_buttonpage_labelframe3_frame1_combobox2,accountingpage_subframe2_frame2_buttonpage_labelframe3_frame1_combobox3,select='month')])

    accountingpage_subframe2_frame2_buttonpage_labelframe3_label2 = Label(accountingpage_subframe2_frame2_buttonpage_labelframe3, text='Description', background=sub_lightdark, fg=text_color,font=('monogram',20))
    accountingpage_subframe2_frame2_buttonpage_labelframe3_label2.grid(column=0,row=1,sticky='nw',pady=5)
    accountingpage_subframe2_frame2_buttonpage_labelframe3_equal2 = Label(accountingpage_subframe2_frame2_buttonpage_labelframe3, text=':', background=sub_lightdark, fg=text_color,font=('monogram',20))
    accountingpage_subframe2_frame2_buttonpage_labelframe3_equal2.grid(column=1,row=1,sticky='nw',pady=5)
    accountingpage_subframe2_frame2_buttonpage_labelframe3_entry2 = Entry(accountingpage_subframe2_frame2_buttonpage_labelframe3, background = light_dark, fg = sub_textcolor,font=('monogram',20),disabledbackground=light_dark,disabledforeground=text_color)
    accountingpage_subframe2_frame2_buttonpage_labelframe3_entry2.insert(0,'\u200BEnter here')
    accountingpage_subframe2_frame2_buttonpage_labelframe3_entry2.bind('<FocusIn>', lambda event: entry_text(accountingpage_subframe2_frame2_buttonpage_labelframe3_entry2,['\u200BEnter here']))
    accountingpage_subframe2_frame2_buttonpage_labelframe3_entry2.bind('<FocusOut>', lambda event: entry_text(accountingpage_subframe2_frame2_buttonpage_labelframe3_entry2,['\u200BEnter here'],True,'\u200BEnter here'))
    accountingpage_subframe2_frame2_buttonpage_labelframe3_entry2.grid(column=2,row=1,sticky='new',pady=5,padx=[0,5])

    accountingpage_subframe2_frame2_buttonpage_labelframe3_label3 = Label(accountingpage_subframe2_frame2_buttonpage_labelframe3, text='Amount', background=sub_lightdark, fg=text_color,font=('monogram',20))
    accountingpage_subframe2_frame2_buttonpage_labelframe3_label3.grid(column=0,row=2,sticky='nw',pady=5)
    accountingpage_subframe2_frame2_buttonpage_labelframe3_equal3 = Label(accountingpage_subframe2_frame2_buttonpage_labelframe3, text=':', background=sub_lightdark, fg=text_color,font=('monogram',20))
    accountingpage_subframe2_frame2_buttonpage_labelframe3_equal3.grid(column=1,row=2,sticky='nw',pady=5)
    accountingpage_subframe2_frame2_buttonpage_labelframe3_entry3 = Entry(accountingpage_subframe2_frame2_buttonpage_labelframe3, background = light_dark, fg = sub_textcolor,font=('monogram',20),disabledbackground=light_dark,disabledforeground=text_color)
    accountingpage_subframe2_frame2_buttonpage_labelframe3_entry3.insert(0,'\u200Beg.1000')
    accountingpage_subframe2_frame2_buttonpage_labelframe3_entry3.bind('<FocusIn>', lambda event: entry_text(accountingpage_subframe2_frame2_buttonpage_labelframe3_entry3,['\u200Beg.1000']))
    accountingpage_subframe2_frame2_buttonpage_labelframe3_entry3.bind('<FocusOut>', lambda event: entry_text(accountingpage_subframe2_frame2_buttonpage_labelframe3_entry3,['\u200Beg.1000'],True,'\u200Beg.1000'))
    accountingpage_subframe2_frame2_buttonpage_labelframe3_entry3.grid(column=2,row=2,sticky='new',pady=5,padx=[0,5])

    # LabelFrame for explanation
    accountingpage_subframe2_frame2_buttonpage_labelframe4 = LabelFrame(accountingpage_subframe2_frame2_buttonpage_frame1, text='Explanation', background=sub_lightdark, fg=text_color,font=('monogram',20,'bold'))
    accountingpage_subframe2_frame2_buttonpage_labelframe4.grid(column=0,row=1,sticky='nsew',rowspan=2,padx=[0,5])

    accountingpage_subframe2_frame2_buttonpage_labelframe4_label1 = Label(accountingpage_subframe2_frame2_buttonpage_labelframe4, text=' - Choose the Type in the From First', background=sub_lightdark, fg=text_color,font=('monogram',20))
    accountingpage_subframe2_frame2_buttonpage_labelframe4_label1.grid(column=0,row=0,sticky='nw',pady=5)

    accountingpage_subframe2_frame2_buttonpage_labelframe4_label2 = Label(accountingpage_subframe2_frame2_buttonpage_labelframe4, text=' - Date format is DD-MM-YY', background=sub_lightdark, fg=text_color,font=('monogram',20))
    accountingpage_subframe2_frame2_buttonpage_labelframe4_label2.grid(column=0,row=1,sticky='nw',pady=5)

    #Confirm and back button frame
    accountingpage_subframe2_frame2_buttonpage_frame1 = Frame(accountingpage_subframe2_frame2_buttonpage, background=sub_lightdark)
    accountingpage_subframe2_frame2_buttonpage_frame1.grid(column=0,row=2,columnspan=2,sticky='nsew',padx=5,pady=5)

    accountingpage_subframe2_frame2_buttonpage_frame1_button1 = Button(accountingpage_subframe2_frame2_buttonpage_frame1,text='Back',foreground=text_color,background=light_dark,font=(custom_font,20,'bold'),command=back_button)
    accountingpage_subframe2_frame2_buttonpage_frame1_button1.grid(column=0,row=0,sticky='nsew')

    accountingpage_subframe2_frame2_buttonpage_frame1_button2 = Button(accountingpage_subframe2_frame2_buttonpage_frame1,text='',foreground=text_color,background=light_dark,font=(custom_font,20,'bold'),command=lambda:button_page_command('add'))
    accountingpage_subframe2_frame2_buttonpage_frame1_button2.grid(column=1,row=0,sticky='nsew')

    accountingpage_subframe2_frame2_buttonpage_frame1.grid_columnconfigure((0,1),weight=1,uniform='a')



    #Right frames
    accountingpage_subframe2_frame2_infopage_rightframe = Frame(accountingpage_subframe2_frame2_infopage, background=light_dark)
    accountingpage_subframe2_frame2_infopage_rightframe.grid(column=1,row=0,sticky='nsew')

    accountingpage_subframe2_frame2_infopage_button1 = Button(accountingpage_subframe2_frame2_infopage_rightframe,text='Add',foreground=text_color,background=light_dark,font=(custom_font,20,'bold'),command = lambda:to_button_page('add') )
    accountingpage_subframe2_frame2_infopage_button1.grid(column=0,row=0,sticky='nsew',ipadx=30)

    accountingpage_subframe2_frame2_infopage_button1 = Button(accountingpage_subframe2_frame2_infopage_rightframe,text='Remove',foreground=text_color,background=light_dark,font=(custom_font,20,'bold'),command= lambda:to_button_page('remove'))
    accountingpage_subframe2_frame2_infopage_button1.grid(column=0,row=1,sticky='nsew',ipadx=30)

    accountingpage_subframe2_frame2_infopage_button1 = Button(accountingpage_subframe2_frame2_infopage_rightframe,text='Edit',foreground=text_color,background=light_dark,font=(custom_font,20,'bold'),command= lambda:to_button_page('edit') )
    accountingpage_subframe2_frame2_infopage_button1.grid(column=0,row=2,sticky='nsew',ipadx=30)

    accountingpage_subframe2_frame2_infopage_button1 = Button(accountingpage_subframe2_frame2_infopage_rightframe,text='Search',foreground=text_color,background=light_dark,font=(custom_font,20,'bold'),command = lambda:to_button_page('search'))
    accountingpage_subframe2_frame2_infopage_button1.grid(column=0,row=3,sticky='nsew',ipadx=30)

    accountingpage_subframe2_frame2_infopage_rightframe.grid_rowconfigure((0,1,2,3),weight=1,uniform='a')
    accountingpage_subframe2_frame2_infopage_rightframe.grid_columnconfigure(0,weight=1)


    master.grid_rowconfigure(0,weight=1)
    master.grid_rowconfigure([1,2],weight=0)
    master.grid_columnconfigure(0,weight=1)
    return accountingpage_subframe2_frame2_treeview, accountingpage_subframe2_frame2_messages_label1,accountingpage_subframe2_frame2_infopage_frame2,accountingpage_subframe2_frame2_infopage_dataframe,accountingpage_subframe2_frame2_buttonpage,calculate_dataframe,accountingpage_subframe2_frame2_infopage_label3,accountingpage_subframe2_frame2_infopage_label5,accountingpage_subframe2_frame2_infopage_label1s
def build_accounting_page_category(master):
    def reset_button_page():
        accountingpage_subframe2_frame3_categorypage_leftframe_frame1_treeview.unbind('<<TreeviewSelect>>')
        accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3_labelframe1_entry1.delete(0,END)
        accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3_labelframe1_entry1.insert(0,'\u200BEnter Here')
        accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3_labelframe1_entry1.configure(fg=sub_textcolor)
        accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3_labelframe1_combobox1.set('')
        accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3_labelframe1_combobox1.configure(values=[])

        accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3_labelframe2_label2.configure(text='0')
        accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3_labelframe2_label4.configure(text='0')
    def to_button_page(type_of_command = str in ['add','remove','edit','search']):
        def treeview_select(event=None,lock=bool,lock2 = bool):
            accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame1.pack_forget()
            accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame2.pack_forget()
            accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3.pack(side='top',fill='both',expand=1)
            focused = accountingpage_subframe2_frame3_categorypage_leftframe_frame1_treeview.focus()
            state.treeview_selected_row_account = focused
            value = accountingpage_subframe2_frame3_categorypage_leftframe_frame1_treeview.item(focused,'values')

            if not value or len(value) < 5:
                return

            accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3_labelframe1_combobox1.set(value[2])
            accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3_labelframe1_entry1.delete(0,END)
            accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3_labelframe1_entry1.insert(0,value[3])
            accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3_labelframe1_entry1.configure(fg=text_color)
            accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3_labelframe2_label2.configure(text=value[4])
            accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3_labelframe2_label4.configure(text=value[5])

            if lock:
                accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3_labelframe1_combobox1.configure(state='disabled')
                accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3_labelframe1_entry1.configure(state='disabled')

            if lock2:
                accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3_labelframe1_combobox1.configure(state='disabled')
            accountingpage_subframe2_frame3_categorypage_leftframe_frame1_treeview.unbind('<<TreeviewSelect>>')

        if getattr(state,'is_online') == False:
            accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame1.pack_forget()
            if type_of_command == 'add':
                reset_button_page()
                accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame2.pack_forget()
                accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3.pack(side='top',fill='both',expand=1)
                accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3_labelframe1_combobox1.configure(state='readonly')
                accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3_labelframe1_entry1.configure(state='normal')
                accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3_frame1_button2.configure(text='Add', command= lambda: button_command('add'))

                accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3_labelframe1_combobox1.configure(values=state.account_type)

            if type_of_command == 'remove':
                reset_button_page()
                accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3.pack_forget()
                accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame2.pack(side='top', fill='both', expand=1)
                accountingpage_subframe2_frame3_categorypage_leftframe_frame1_treeview.bind('<<TreeviewSelect>>',lambda event :treeview_select(event=event,lock=True))

                accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3_labelframe1_combobox1.configure(state='readonly')
                accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3_labelframe1_entry1.configure(state='normal')
                accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3_frame1_button2.configure(text='Remove', command= lambda: button_command('remove'))

            if type_of_command == 'edit':
                reset_button_page()
                accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3.pack_forget()
                accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame2.pack(side='top',fill='both',expand=1)
                accountingpage_subframe2_frame3_categorypage_leftframe_frame1_treeview.bind('<<TreeviewSelect>>',lambda event :treeview_select(event=event,lock=False,lock2=True))

                accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3_labelframe1_combobox1.configure(state='readonly')
                accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3_labelframe1_entry1.configure(state='normal')
                accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3_frame1_button2.configure(text='Edit', command = lambda: button_command('edit'))

                accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3_labelframe1_combobox1.configure(values=state.account_type)

            if type_of_command == 'search':
                reset_button_page()
                accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame2.pack_forget()
                accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3.pack(side='top',fill='both',expand=1)

                accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3_labelframe1_combobox1.configure(state='readonly')
                accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3_labelframe1_entry1.configure(state='normal')
                accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3_frame1_button2.configure(text='Search',command = lambda: button_command('search'))

                account_type =  [''] + state.account_type 
                accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3_labelframe1_combobox1.configure(values=account_type)
    def button_command(type_of_command = str in ['add','remove','edit','search']):
        def warning_message(type_of_command = str in ['remove','edit']):
            def countdown(seconds_left):
                if not result_label4.winfo_exists():
                    return
                if seconds_left > 0:
                    result_label4.configure(text=f'You can confirm in {seconds_left} seconds')
                    master.after(1000, countdown, seconds_left - 1)
                else:
                    result_label4.configure(text=f'You can confirm.', fg = success_color)
                    if type_of_command == 'remove':
                        result_frame1_button2.configure(command=confirm_button_delete)
                    else:
                        result_frame1_button2.configure(command=confirm_button_edit)
            def confirm_button_delete():
                # Grab the account_id before threading
                account_id = accountingpage_subframe2_frame3_categorypage_leftframe_frame1_treeview.item(
                    state.treeview_selected_row_account, 'values'
                )[1]

                def worker():
                    # Run heavy DB delete here
                    api.offline_remove_account(
                        account_id,
                        accountingpage_subframe2_frame3_categorypage_leftframe_frame2_label1,
                        accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3_labelframe1_combobox1
                    )

                    # Once done, update UI safely back in main thread
                    master.after(0, finish_delete_ui)

                Thread(target=worker, daemon=True).start()


            def finish_delete_ui():
                result.destroy()
                tree = accountingpage_subframe2_frame3_categorypage_leftframe_frame1_treeview

                # Remove from treeview
                tree.delete(state.treeview_selected_row_account)

                # Update account list
                status, new_lists = api.offline_update_account(
                    tree,
                    accountingpage_subframe2_frame3_categorypage_leftframe_frame2_label1
                )

                if status:
                    # Clear and repopulate
                    for row in tree.get_children():
                        tree.delete(row)

                    for i, value in enumerate(new_lists):
                        input_list = (i + 1,) + value
                        tree.insert('', 'end', values=input_list)

                    # Update labels
                    try:
                        num = float(accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame1_labelframe1_label2.cget('text')) - float(
                            accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3_labelframe2_label4.cget('text')
                        )
                        accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame1_labelframe1_label2.configure(text=str(num))

                        count = int(accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame1_labelframe1_label4.cget('text')) - 1
                        accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame1_labelframe1_label4.configure(text=str(count))
                    except Exception as e:
                        print("UI update error:", e)

                # Refresh button page
                window.after(0, lambda: [to_button_page('remove'), master.update_idletasks()])
            def confirm_button_edit():
                result.destroy()
                values = list(accountingpage_subframe2_frame3_categorypage_leftframe_frame1_treeview.item(state.treeview_selected_row_account,'values'))
                results, data = api.offline_edit_account(accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3_labelframe1_combobox1,accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3_labelframe1_entry1,accountingpage_subframe2_frame3_categorypage_leftframe_frame2_label1,values[1])
                if results == True:
                    status , data = api.offline_update_account(accountingpage_subframe2_frame3_categorypage_leftframe_frame1_treeview,accountingpage_subframe2_frame3_categorypage_leftframe_frame2_label1)
                    for i in accountingpage_subframe2_frame3_categorypage_leftframe_frame1_treeview.get_children():
                        accountingpage_subframe2_frame3_categorypage_leftframe_frame1_treeview.delete(i)

                    for index, values in enumerate(data):
                        values = (index+1,) + values
                        accountingpage_subframe2_frame3_categorypage_leftframe_frame1_treeview.insert('','end',values= values)

                master.after(0,lambda :[to_button_page('edit'),master.update_idletasks()])

            MessageBeep(MB_OK)
            result = Toplevel(master,background=sub_lightdark)
            result.title('Warning Message')
            result.resizable(False,False)
            result.transient(master)
            result.grab_set()
            result.focus_force()
            master.update_idletasks()

            # Get master window position and size
            master_x = master.winfo_rootx()
            master_y = master.winfo_rooty()
            master_width = master.winfo_width()
            master_height = master.winfo_height()

            # Calculate position
            x = master_x + (master_width // 2) - (500 // 2)
            y = master_y + (master_height // 2) - (200 // 2)

            # Apply new position
            result.geometry(f"{500}x{200}+{x}+{y}")
            result.grid_columnconfigure(1,weight=1)

            result_label0 = Label(result, text='!', background=sub_lightdark, fg=error_color,font=('monogram',25,'bold'))
            result_label0.grid(column=0,row=0,sticky='nsw',pady=[5,0],padx=[5,0],ipady=5,ipadx=10)

            result_label1 = Label(result, text='Confirm Account Deletion?', background=sub_lightdark, fg=text_color,font=('monogram',25,'bold'))
            result_label1.grid(column=1,row=0,sticky='nsw',pady=[5,0],padx=[0,5])

            result_label2 = Label(result, text='This account and all RELATED transactions', background=sub_lightdark, fg=text_color,font=('monogram',18))
            result_label2.grid(column=1,row=1,sticky='sw',padx=5)

            result_label3 = Label(result, text='will be PERMANTLY DELETED!', background=sub_lightdark, fg=text_color,font=('monogram',18))
            result_label3.grid(column=1,row=2,sticky='nw',padx=5)

            result_label4 = Label(result, text='You can confirm in 10 seconds.', background=sub_lightdark, fg=error_color,font=('monogram',18))
            result_label4.grid(column=1,row=3,sticky='nw',padx=5)

            result_frame1 = Frame(result,background=sub_lightdark)
            result_frame1.grid(column=0,row=4,sticky='nsew',padx=5,pady=[30,0],columnspan=2)
            result_frame1.grid_columnconfigure([0,1],weight=1,uniform='a')

            result_frame1_button1 = Button(result_frame1,text='Back',foreground=text_color,background=light_dark,font=(custom_font,20,'bold'),command=lambda:result.destroy())
            result_frame1_button1.grid(column=0,row=0,sticky='nsew',padx=5)

            result_frame1_button2 = Button(result_frame1,text='Confirm',foreground=text_color,background=light_dark,font=(custom_font,20,'bold'),command=None)
            result_frame1_button2.grid(column=1,row=0,sticky='nsew',padx=[0,5])
            countdown(10)
            if type_of_command == 'remove':
                result_label1.configure(text='Confirm Account Deletion?')
                result_label3.configure(text='will be PERMANTLY DELETED!')
            else:
                result_label1.configure(text='Confirm Account Edit?')
                result_label3.configure(text='will be PERMANTLY CHANGED!')

        if getattr(state,'is_online') == False:
            if type_of_command == 'add':
                status, data = api.offline_add_account(accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3_labelframe1_combobox1,accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3_labelframe1_entry1,accountingpage_subframe2_frame3_categorypage_leftframe_frame2_label1)
                if status:
                    accountingpage_subframe2_frame3_categorypage_leftframe_frame1_treeview.insert('','end',values=([len(accountingpage_subframe2_frame3_categorypage_leftframe_frame1_treeview.get_children())+1] + data))
                    try:
                        count = int(accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame1_labelframe1_label4.cget('text')) + 1
                        accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame1_labelframe1_label4.configure(text=str(count))
                    except Exception as e:
                        print(str(e))

                    to_button_page('add')

            if type_of_command == 'remove':
                warning_message('remove')

            if type_of_command == 'edit':
                warning_message('edit')

            if type_of_command == 'search':
                def search_account():
                    def worker():
                        status, data = api.offline_search_account(
                            accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3_labelframe1_combobox1,
                            accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3_labelframe1_entry1,
                            accountingpage_subframe2_frame3_categorypage_leftframe_frame2_label1
                        )
                        master.after(0, lambda: update_treeview_with_search(status, data))

                    Thread(target=worker, daemon=True).start()


                def update_treeview_with_search(status, data):
                    tree = accountingpage_subframe2_frame3_categorypage_leftframe_frame1_treeview
                    if status:
                        # Clear old rows
                        for row in tree.get_children():
                            tree.delete(row)

                        # Insert in chunks (to avoid freezing UI with huge datasets)
                        def insert_chunk(start=0, chunk_size=500):
                            end = min(start + chunk_size, len(data))
                            for index, value in enumerate(data[start:end], start=start):
                                added_list = (index + 1,) + value
                                tree.insert('', 'end', values=added_list)

                            if end < len(data):
                                master.after(1, insert_chunk, end)  # schedule next chunk

                        insert_chunk()

                search_account()

    def back_button():
        for frame in [accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame2,accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3]:
            frame.pack_forget()
        accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame1.pack(side='top',fill='both',expand=1)

    master.grid_columnconfigure(0,weight=1)
    master.grid_rowconfigure(0,weight=1)
    accountingpage_subframe2_frame3_categorypage = Frame(master, background=sub_lightdark)
    accountingpage_subframe2_frame3_categorypage.grid(column=0,row=0,sticky='nsew')
    accountingpage_subframe2_frame3_categorypage.grid_columnconfigure(0,weight=13,uniform='a')
    accountingpage_subframe2_frame3_categorypage.grid_columnconfigure(1,weight=11,uniform='a')
    accountingpage_subframe2_frame3_categorypage.grid_rowconfigure(0,weight=1)

    #Left Frame
    accountingpage_subframe2_frame3_categorypage_leftframe = Frame(accountingpage_subframe2_frame3_categorypage, background=sub_lightdark)
    accountingpage_subframe2_frame3_categorypage_leftframe.grid(column=0,row=0,sticky='nsew',padx=[0,3])
    accountingpage_subframe2_frame3_categorypage_leftframe.grid_columnconfigure(0,weight=1)
    accountingpage_subframe2_frame3_categorypage_leftframe.grid_columnconfigure(1,weight=0)
    accountingpage_subframe2_frame3_categorypage_leftframe.grid_rowconfigure(0,weight=1)


    accountingpage_subframe2_frame3_categorypage_leftframe_frame1 = Frame(accountingpage_subframe2_frame3_categorypage_leftframe, background='black')
    accountingpage_subframe2_frame3_categorypage_leftframe_frame1.grid_columnconfigure(0,weight=1)
    accountingpage_subframe2_frame3_categorypage_leftframe_frame1.grid_rowconfigure(0,weight=1)
    accountingpage_subframe2_frame3_categorypage_leftframe_frame1.grid(column=0,row=0,sticky='nsew',columnspan=2,pady=[0,5])

    accountingpage_subframe2_frame3_categorypage_leftframe_frame1_scrollbar = ttk.Scrollbar(accountingpage_subframe2_frame3_categorypage_leftframe_frame1)
    accountingpage_subframe2_frame3_categorypage_leftframe_frame1_scrollbar.grid(column=1,row=0,sticky='nsew')

    headings = ('No.','ID','Type','Account','Entry Count','Balance')
    
    accountingpage_subframe2_frame3_categorypage_leftframe_frame1_treeview = ttk.Treeview(accountingpage_subframe2_frame3_categorypage_leftframe_frame1,columns=headings, show='headings',yscrollcommand=accountingpage_subframe2_frame3_categorypage_leftframe_frame1_scrollbar)
    accountingpage_subframe2_frame3_categorypage_leftframe_frame1_treeview.grid(column=0,row=0,sticky='nsew')
    accountingpage_subframe2_frame3_categorypage_leftframe_frame1_scrollbar.configure(command=accountingpage_subframe2_frame3_categorypage_leftframe_frame1_treeview.yview)

    accountingpage_subframe2_frame3_categorypage_leftframe_frame1_treeview.column('No.',anchor='w',stretch=True,minwidth=35,width=35)
    accountingpage_subframe2_frame3_categorypage_leftframe_frame1_treeview.heading('No.', text = 'No.')

    accountingpage_subframe2_frame3_categorypage_leftframe_frame1_treeview.column('ID',anchor='w',stretch=True,minwidth=35,width=35)
    accountingpage_subframe2_frame3_categorypage_leftframe_frame1_treeview.heading('ID', text = 'ID')

    accountingpage_subframe2_frame3_categorypage_leftframe_frame1_treeview.column('Type',anchor='w',stretch=True,minwidth=50,width=100)
    accountingpage_subframe2_frame3_categorypage_leftframe_frame1_treeview.heading('Type', text = 'Type')

    accountingpage_subframe2_frame3_categorypage_leftframe_frame1_treeview.column('Account',anchor='w',stretch=True,minwidth=50,width=100)
    accountingpage_subframe2_frame3_categorypage_leftframe_frame1_treeview.heading('Account', text = 'Account')

    accountingpage_subframe2_frame3_categorypage_leftframe_frame1_treeview.column('Entry Count',anchor='w',stretch=True,minwidth=50,width=100)
    accountingpage_subframe2_frame3_categorypage_leftframe_frame1_treeview.heading('Entry Count', text = 'Entry Count')

    accountingpage_subframe2_frame3_categorypage_leftframe_frame1_treeview.column('Balance',anchor='w',stretch=True,minwidth=50,width=150)
    accountingpage_subframe2_frame3_categorypage_leftframe_frame1_treeview.heading('Balance', text = 'Balance')

    #Message frame 
    accountingpage_subframe2_frame3_categorypage_leftframe_frame2 = Frame(accountingpage_subframe2_frame3_categorypage_leftframe, background=light_dark)
    accountingpage_subframe2_frame3_categorypage_leftframe_frame2.grid(column=0,row=1,sticky='nsew',columnspan=2)

    accountingpage_subframe2_frame3_categorypage_leftframe_frame2_border = Frame(accountingpage_subframe2_frame3_categorypage_leftframe_frame2, background=sub_lightdark)
    accountingpage_subframe2_frame3_categorypage_leftframe_frame2_border.pack(side='top',fill='both', expand=True,pady=(3,0),padx=3,anchor='w')

    accountingpage_subframe2_frame3_categorypage_leftframe_frame2_label1 = Label(accountingpage_subframe2_frame3_categorypage_leftframe_frame2_border, text='', background=sub_lightdark, fg=error_color,font=('monogram',20))
    accountingpage_subframe2_frame3_categorypage_leftframe_frame2_label1.pack(side='left',anchor='w')

    #Bottom Frames
    accountingpage_subframe2_frame3_categorypage_leftframe_frame3 = Frame(accountingpage_subframe2_frame3_categorypage_leftframe, background=light_dark,height=316)
    accountingpage_subframe2_frame3_categorypage_leftframe_frame3.pack_propagate(False)
    accountingpage_subframe2_frame3_categorypage_leftframe_frame3.grid_columnconfigure(0,weight=1)
    accountingpage_subframe2_frame3_categorypage_leftframe_frame3.grid_rowconfigure(0,weight=1)
    accountingpage_subframe2_frame3_categorypage_leftframe_frame3.grid(column=0,row=2,sticky='nsew')

    #Data Frame
    accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame1 = Frame(accountingpage_subframe2_frame3_categorypage_leftframe_frame3, background=light_dark)
    accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame1.pack(side='top',expand=True,fill='both')

    accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame1_labelframe1 = LabelFrame(accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame1, background=sub_lightdark,text='Data',font=('monogram',20,'bold'),fg=text_color)
    accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame1_labelframe1.grid_columnconfigure(2,weight=1)
    accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame1_labelframe1.pack(side='top',fill='both',expand=1,pady=3,padx=[3,0])

    accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame1_labelframe1_label1 = Label(accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame1_labelframe1, text='Total Amount Displayed', background=sub_lightdark, fg=text_color,font=('monogram',20))
    accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame1_labelframe1_label1.grid(column=0,row=0,sticky='nw',pady=5,padx=[3,0])
    accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame1_labelframe1_equal1 = Label(accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame1_labelframe1, text=':', background=sub_lightdark, fg=text_color,font=('monogram',20))
    accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame1_labelframe1_equal1.grid(column=1,row=0,sticky='nw',pady=5)
    accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame1_labelframe1_label2 = Label(accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame1_labelframe1, text='0', background=sub_lightdark, fg=text_color,font=('monogram',20,'bold'))
    accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame1_labelframe1_label2.grid(column=2,row=0,sticky='nw',pady=5)

    accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame1_labelframe1_label3 = Label(accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame1_labelframe1, text='Total Account Displayed', background=sub_lightdark, fg=text_color,font=('monogram',20))
    accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame1_labelframe1_label3.grid(column=0,row=1,sticky='nw',pady=5,padx=[3,0])
    accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame1_labelframe1_equal2 = Label(accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame1_labelframe1, text=':', background=sub_lightdark, fg=text_color,font=('monogram',20))
    accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame1_labelframe1_equal2.grid(column=1,row=1,sticky='nw',pady=5)
    accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame1_labelframe1_label4 = Label(accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame1_labelframe1, text='0', background=sub_lightdark, fg=text_color,font=('monogram',20,'bold'))
    accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame1_labelframe1_label4.grid(column=2,row=1,sticky='nw',pady=5)


    #Please choose to pick Frame
    accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame2 = Frame(accountingpage_subframe2_frame3_categorypage_leftframe_frame3, background=light_dark)
    accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame2.grid_rowconfigure(0,weight=1)
    accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame2.grid_columnconfigure(0,weight=1)

    accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame2_label1 = Label(accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame2,background=sub_lightdark,fg=text_color,font=('monogram',20,'bold'),text='Please click on the row\n you want to change')
    accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame2_label1.grid(column=0,row=0,sticky='nsew',padx=[3,0],pady=[3,0])

    accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame2_button1 = Button(accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame2,text='Back',foreground=text_color,background=light_dark,font=(custom_font,20,'bold'),command=back_button)
    accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame2_button1.grid(column=0,row=1,sticky='nsew',padx=[3,0],pady=3)

    #lower left Frame
    accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3 = Frame(accountingpage_subframe2_frame3_categorypage_leftframe_frame3, background=light_dark)
    accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3.grid_rowconfigure([0,1],weight=1)
    accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3.grid_columnconfigure(0,weight=1)

    #Classification LabelFrame
    accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3_labelframe1 = LabelFrame(accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3,background = sub_lightdark,text='Classification',font=('monogram',20,'bold'),fg=text_color)
    accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3_labelframe1.grid(column=0,row=0,sticky='nsew',padx=[3,0],pady=3)
    accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3_labelframe1.grid_rowconfigure([0,1],weight=1)
    accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3_labelframe1.grid_columnconfigure(2,weight=1)

    accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3_labelframe1_label1 = Label(accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3_labelframe1, text='Type', background=sub_lightdark, fg=text_color,font=('monogram',20))
    accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3_labelframe1_label1.grid(column=0,row=0,sticky='nw',pady=5,padx=[3,0])
    accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3_labelframe1_equal1 = Label(accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3_labelframe1, text=':', background=sub_lightdark, fg=text_color,font=('monogram',20))
    accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3_labelframe1_equal1.grid(column=1,row=0,sticky='nw',pady=5)
    accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3_labelframe1_combobox1 = ttk.Combobox(accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3_labelframe1, background = light_dark, foreground = text_color,font=('monogram',20),state='readonly',justify='left')
    accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3_labelframe1_combobox1.grid(column=2,row=0,sticky='new',pady=5,padx=[0,5])

    accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3_labelframe1_label2 = Label(accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3_labelframe1, text='Account     ', background=sub_lightdark, fg=text_color,font=('monogram',20))
    accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3_labelframe1_label2.grid(column=0,row=1,sticky='nw',pady=5,padx=[3,0])
    accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3_labelframe1_equal2 = Label(accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3_labelframe1, text=':', background=sub_lightdark, fg=text_color,font=('monogram',20))
    accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3_labelframe1_equal2.grid(column=1,row=1,sticky='nw',pady=5)
    accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3_labelframe1_entry1 = Entry(accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3_labelframe1, background = light_dark, fg = sub_textcolor,font=('monogram',20),disabledbackground=light_dark,disabledforeground=text_color)
    accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3_labelframe1_entry1.insert(0,'\u200BEnter Here')
    accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3_labelframe1_entry1.bind('<FocusIn>', lambda event: entry_text(accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3_labelframe1_entry1,['\u200BEnter Here']))
    accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3_labelframe1_entry1.bind('<FocusOut>', lambda event: entry_text(accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3_labelframe1_entry1,['\u200BEnter Here'],True,'\u200BEnter Here'))
    accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3_labelframe1_entry1.grid(column=2,row=1,sticky='new',pady=5,padx=[0,5])
    
    #Values LabelFrame
    accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3_labelframe2 = LabelFrame(accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3,background = sub_lightdark,text='Data',font=('monogram',20,'bold'),fg=text_color)
    accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3_labelframe2.grid(column=0,row=1,sticky='nsew',padx=[3,0],pady=[0,3])
    accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3_labelframe2.grid_columnconfigure(2,weight=1)

    accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3_labelframe2_label1 = Label(accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3_labelframe2, text='Entry Count', background=sub_lightdark, fg=text_color,font=('monogram',20))
    accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3_labelframe2_label1.grid(column=0,row=0,sticky='nw',pady=5,padx=[3,0])
    accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3_labelframe2_equal1 = Label(accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3_labelframe2, text=':', background=sub_lightdark, fg=text_color,font=('monogram',20))
    accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3_labelframe2_equal1.grid(column=1,row=0,sticky='nw',pady=5)
    accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3_labelframe2_label2 = Label(accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3_labelframe2, text='0', background=sub_lightdark, fg=text_color,font=('monogram',20,'bold'))
    accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3_labelframe2_label2.grid(column=2,row=0,sticky='nw',pady=5)

    accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3_labelframe2_label3 = Label(accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3_labelframe2, text='Balance Tied', background=sub_lightdark, fg=text_color,font=('monogram',20))
    accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3_labelframe2_label3.grid(column=0,row=1,sticky='nw',pady=5,padx=[3,0])
    accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3_labelframe2_equal2 = Label(accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3_labelframe2, text=':', background=sub_lightdark, fg=text_color,font=('monogram',20))
    accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3_labelframe2_equal2.grid(column=1,row=1,sticky='nw',pady=5)
    accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3_labelframe2_label4 = Label(accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3_labelframe2, text='0', background=sub_lightdark, fg=text_color,font=('monogram',20,'bold'))
    accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3_labelframe2_label4.grid(column=2,row=1,sticky='nw',pady=5)

    #button Frame
    accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3_frame1 = Frame(accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3, background=light_dark)
    accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3_frame1.grid(column=0,row=2,sticky='nsew',padx=3,pady=[0,3])
    accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3_frame1.grid_columnconfigure([0,1],weight=1,uniform='a')
    accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3_frame1.grid_rowconfigure(0,weight=1)

    accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3_frame1_button1 = Button(accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3_frame1,text='Back',foreground=text_color,background=light_dark,font=(custom_font,20,'bold'),command=back_button)
    accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3_frame1_button1.grid(column=0,row=0,sticky='nsew')

    accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3_frame1_button2 = Button(accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3_frame1,text='',foreground=text_color,background=light_dark,font=(custom_font,20,'bold'))
    accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3_frame1_button2.grid(column=1,row=0,sticky='nsew')

    #lower Button Frame
    accountingpage_subframe2_frame3_categorypage_leftframe_frame4= Frame(accountingpage_subframe2_frame3_categorypage_leftframe, background=light_dark,height=316)
    accountingpage_subframe2_frame3_categorypage_leftframe_frame4.grid_columnconfigure(0,weight=1)
    accountingpage_subframe2_frame3_categorypage_leftframe_frame4.grid_rowconfigure([0,1,2,3],weight=1,uniform='a')
    accountingpage_subframe2_frame3_categorypage_leftframe_frame4.grid(column=1,row=2,sticky='nsew')

    accountingpage_subframe2_frame3_categorypage_leftframe_frame4_button1 = Button(accountingpage_subframe2_frame3_categorypage_leftframe_frame4,text='Add',foreground=text_color,background=light_dark,font=(custom_font,20,'bold'),command = lambda: to_button_page('add'))
    accountingpage_subframe2_frame3_categorypage_leftframe_frame4_button1.grid(column=0,row=0,sticky='nsew',pady=[3,3],padx=3,ipadx=30)

    accountingpage_subframe2_frame3_categorypage_leftframe_frame4_button2 = Button(accountingpage_subframe2_frame3_categorypage_leftframe_frame4,text='Remove',foreground=text_color,background=light_dark,font=(custom_font,20,'bold'),command = lambda: to_button_page('remove'))
    accountingpage_subframe2_frame3_categorypage_leftframe_frame4_button2.grid(column=0,row=1,sticky='nsew',pady=[0,3],padx=3,ipadx=30)

    accountingpage_subframe2_frame3_categorypage_leftframe_frame4_button3 = Button(accountingpage_subframe2_frame3_categorypage_leftframe_frame4,text='Edit',foreground=text_color,background=light_dark,font=(custom_font,20,'bold'),command = lambda: to_button_page('edit'))
    accountingpage_subframe2_frame3_categorypage_leftframe_frame4_button3.grid(column=0,row=2,sticky='nsew',pady=[0,3],padx=3,ipadx=30)

    accountingpage_subframe2_frame3_categorypage_leftframe_frame4_button4 = Button(accountingpage_subframe2_frame3_categorypage_leftframe_frame4,text='Search',foreground=text_color,background=light_dark,font=(custom_font,20,'bold'),command = lambda: to_button_page('search'))
    accountingpage_subframe2_frame3_categorypage_leftframe_frame4_button4.grid(column=0,row=3,sticky='nsew',pady=[0,3],padx=3,ipadx=30)

    # Right Frmae
    def graph_plotting():
        start_day = accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2_labelframe1_frame1_combobox1.get() or "0"
        start_month = accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2_labelframe1_frame1_combobox2.get() or "0"
        start_year = accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2_labelframe1_frame1_combobox3.get() or "0"
        start_date = f'{start_day}-{start_month}-{start_year}'

        end_day = accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2_labelframe1_frame2_combobox1.get() or "0"
        end_month = accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2_labelframe1_frame2_combobox2.get() or "0"
        end_year = accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2_labelframe1_frame2_combobox3.get() or "0"
        end_date = f'{end_day}-{end_month}-{end_year}'


        status, data, graph_type, line_color = api.offline_graph_plotting(start_date,end_date,accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2_labelframe2_combobox3,accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2_labelframe2_combobox4,accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2_labelframe2_combobox1,accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame1_label1,accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2_labelframe2_combobox2)
        if status:
            ax.plot(data[1],data[0], marker='.', linestyle='-', color=line_color,label = f'= {graph_type} ({accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2_labelframe2_combobox3.get()},{accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2_labelframe2_combobox4.get()})')
            ax.set_xticks([data[1][0],data[1][len(data[1])//3],data[1][len(2*data[1])//3],data[1][-1]])
            ax.legend(loc = 'lower right', fontsize=5)
            for text in ax.legend().get_texts():
                text.set_color("black")
                text.set_fontsize(15)
            canvas.draw_idle()
    def set_custom_combobox_value(widget,fetched_widget,setup):
        if not setup:
            widget.set('')
        value = fetched_widget.get()
        if len(value) > 0:
            placed_value = api.offline_fetch_account_from_type(value)
            widget.configure(values=[''] + placed_value)
    def clear_graph_plot():
        ax.clear()
        ax.grid(True,'major',color='black', linestyle='-', linewidth=1)
        ax.set_xlabel('Date')
        ax.set_ylabel('Amount' )
        ax.set_title('Daily Data')
        canvas.draw_idle()
    accountingpage_subframe2_frame3_categorypage_rightframe = Frame(accountingpage_subframe2_frame3_categorypage, background=sub_lightdark)
    accountingpage_subframe2_frame3_categorypage_rightframe.grid(column=1,row=0,sticky='nsew',padx=[5,0])
    accountingpage_subframe2_frame3_categorypage_rightframe.grid_columnconfigure(0,weight=1)
    accountingpage_subframe2_frame3_categorypage_rightframe.grid_rowconfigure(0,weight=1)

    accountingpage_subframe2_frame3_categorypage_rightframe_canvasframe = Frame(accountingpage_subframe2_frame3_categorypage_rightframe, background=light_dark)
    accountingpage_subframe2_frame3_categorypage_rightframe_canvasframe.grid_rowconfigure(0,weight=1)
    accountingpage_subframe2_frame3_categorypage_rightframe_canvasframe.grid_columnconfigure(0,weight=1)
    accountingpage_subframe2_frame3_categorypage_rightframe_canvasframe.grid(column=0,row=0,sticky='nsew')
    accountingpage_subframe2_frame3_categorypage_rightframe_canvasframe.grid_propagate(False)

    fig = Figure(figsize=(10,4), dpi=100)
    fig.patch.set_facecolor(color=sub_lightdark)
    ax = fig.add_subplot(111)
    ax.grid(True,'major',color='black', linestyle='-', linewidth=1)
    ax.set_facecolor('white')
    ax.set_xlabel('Date')
    ax.set_ylabel('Amount' )
    ax.set_title('Daily Data')
    ax.spines['top'].set_color(sub_lightdark)
    ax.spines['bottom'].set_color("white")
    ax.spines['left'].set_color("white")
    ax.spines['right'].set_color(sub_lightdark)
    
    canvas = FigureCanvasTkAgg(fig, master =accountingpage_subframe2_frame3_categorypage_rightframe_canvasframe )
    canvas.get_tk_widget().grid(column=0,row=0,sticky='nsew',padx=3,pady=3)

    accountingpage_subframe2_frame3_categorypage_rightframe_frame1 = Frame(accountingpage_subframe2_frame3_categorypage_rightframe, background=light_dark,height=346)
    accountingpage_subframe2_frame3_categorypage_rightframe_frame1.grid_propagate(False)
    accountingpage_subframe2_frame3_categorypage_rightframe_frame1.grid_columnconfigure(0,weight=1)
    accountingpage_subframe2_frame3_categorypage_rightframe_frame1.grid_rowconfigure(1,weight=1)
    accountingpage_subframe2_frame3_categorypage_rightframe_frame1.grid(column=0,row=1,sticky='nsew',pady=[5,0])

    #Message Frame:
    accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame1 = Frame(accountingpage_subframe2_frame3_categorypage_rightframe_frame1, background=sub_lightdark)
    accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame1.grid(column=0,row=0,sticky='nsew',padx=3,pady=3)

    accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame1_label1 = Label(accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame1, text='', background=sub_lightdark, fg=error_color,font=('monogram',20))
    accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame1_label1.pack(side='left',anchor='w')

    #Data Frame
    accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2 = Frame(accountingpage_subframe2_frame3_categorypage_rightframe_frame1, background=sub_lightdark)
    accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2.grid_columnconfigure([0],weight=1)
    accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2.grid_rowconfigure([0,1],weight=1)
    accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2.grid(column=0,row=1,sticky='nsew',padx=3,pady=[0,3])
    
    accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2_labelframe1 = LabelFrame(accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2,background=sub_lightdark,text='Date Range',font=(custom_font,20,'bold'),fg=text_color)
    accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2_labelframe1.grid_columnconfigure([0,2],weight=1)
    accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2_labelframe1.grid(column=0,row=0,sticky='nsew')

    accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2_labelframe1_label1 = Label(accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2_labelframe1, text='Start Date', background=sub_lightdark, fg=text_color,font=('monogram',20))
    accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2_labelframe1_label1.grid(column=0,row=0,sticky='nw',pady=5,padx=3)
    accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2_labelframe1_equal1 = Label(accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2_labelframe1, text=':', background=sub_lightdark, fg=text_color,font=('monogram',20))
    accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2_labelframe1_equal1.grid(column=1,row=0,sticky='nw',pady=5,padx=3)
    accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2_labelframe1_frame1 = Frame(accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2_labelframe1,background=sub_lightdark)
    accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2_labelframe1_frame1.grid(column=2,row=0,sticky='new',pady=5,padx=[0,5])
    accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2_labelframe1_frame1_combobox1 = ttk.Combobox(accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2_labelframe1_frame1, background = light_dark, foreground = text_color,font=('monogram',20),state='readonly',justify='left',width=5)
    accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2_labelframe1_frame1_combobox1.pack(side='left')
    accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2_labelframe1_frame1_combobox2 = ttk.Combobox(accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2_labelframe1_frame1, background = light_dark, foreground = text_color,font=('monogram',20),state='readonly',justify='left',width=5)
    accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2_labelframe1_frame1_combobox2.pack(side='left',padx=5)
    accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2_labelframe1_frame1_combobox3 = ttk.Combobox(accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2_labelframe1_frame1, background = light_dark, foreground = text_color,font=('monogram',20),state='readonly',justify='left',width=7)
    accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2_labelframe1_frame1_combobox3.pack(side='left')
    combobox_date_set_year(accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2_labelframe1_frame1_combobox3)
    accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2_labelframe1_frame1_combobox3.bind('<<ComboboxSelected>>', lambda e: [combobox_date(accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2_labelframe1_frame1_combobox1,accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2_labelframe1_frame1_combobox2,accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2_labelframe1_frame1_combobox3,select='year')])
    accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2_labelframe1_frame1_combobox2.bind('<<ComboboxSelected>>', lambda e: [combobox_date(accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2_labelframe1_frame1_combobox1,accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2_labelframe1_frame1_combobox2,accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2_labelframe1_frame1_combobox3,select='month')])

    accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2_labelframe1_label2 = Label(accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2_labelframe1, text='End Date', background=sub_lightdark, fg=text_color,font=('monogram',20))
    accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2_labelframe1_label2.grid(column=0,row=1,sticky='nw',pady=5,padx=3)
    accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2_labelframe1_equal2 = Label(accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2_labelframe1, text=':', background=sub_lightdark, fg=text_color,font=('monogram',20))
    accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2_labelframe1_equal2.grid(column=1,row=1,sticky='nw',pady=5,padx=3)
    accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2_labelframe1_frame2 = Frame(accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2_labelframe1,background=sub_lightdark)
    accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2_labelframe1_frame2.grid(column=2,row=1,sticky='new',pady=5,padx=[0,5])
    accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2_labelframe1_frame2_combobox1 = ttk.Combobox(accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2_labelframe1_frame2, background = light_dark, foreground = text_color,font=('monogram',20),state='readonly',justify='left',width=5)
    accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2_labelframe1_frame2_combobox1.pack(side='left')
    accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2_labelframe1_frame2_combobox2 = ttk.Combobox(accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2_labelframe1_frame2, background = light_dark, foreground = text_color,font=('monogram',20),state='readonly',justify='left',width=5)
    accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2_labelframe1_frame2_combobox2.pack(side='left',padx=5)
    accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2_labelframe1_frame2_combobox3 = ttk.Combobox(accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2_labelframe1_frame2, background = light_dark, foreground = text_color,font=('monogram',20),state='readonly',justify='left',width=7)
    accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2_labelframe1_frame2_combobox3.pack(side='left')
    combobox_date_set_year(accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2_labelframe1_frame2_combobox3)
    accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2_labelframe1_frame2_combobox3.bind('<<ComboboxSelected>>', lambda e: [combobox_date(accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2_labelframe1_frame2_combobox1,accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2_labelframe1_frame2_combobox2,accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2_labelframe1_frame2_combobox3,select='year')])
    accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2_labelframe1_frame2_combobox2.bind('<<ComboboxSelected>>', lambda e: [combobox_date(accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2_labelframe1_frame2_combobox1,accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2_labelframe1_frame2_combobox2,accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2_labelframe1_frame2_combobox3,select='month')])

    accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2_labelframe2 = LabelFrame(accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2,background=sub_lightdark,text='Classification',font=(custom_font,20,'bold'),fg=text_color)
    accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2_labelframe2.grid_columnconfigure([0,2],weight=1)
    accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2_labelframe2.grid(column=0,row=1,sticky='nsew')

    accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2_labelframe2_label1 = Label(accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2_labelframe2, text='Graph Data', background=sub_lightdark, fg=text_color,font=('monogram',20))
    accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2_labelframe2_label1.grid(column=0,row=0,sticky='nw',pady=5,padx=3)
    accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2_labelframe2_equal1 = Label(accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2_labelframe2, text=':', background=sub_lightdark, fg=text_color,font=('monogram',20))
    accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2_labelframe2_equal1.grid(column=1,row=0,sticky='nw',pady=5,padx=3)
    accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2_labelframe2_combobox1 = ttk.Combobox(accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2_labelframe2,state='readonly',font = (custom_font,20),values=['Amount','Total Amount','Entry Count'])
    accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2_labelframe2_combobox1.grid(column=2,row=0,sticky='nsew',pady=5,padx=[0,5])

    accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2_labelframe2_label2 = Label(accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2_labelframe2, text='Graph Line Color', background=sub_lightdark, fg=text_color,font=('monogram',20))
    accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2_labelframe2_label2.grid(column=0,row=2,sticky='nw',pady=5,padx=3)
    accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2_labelframe2_equal2 = Label(accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2_labelframe2, text=':', background=sub_lightdark, fg=text_color,font=('monogram',20))
    accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2_labelframe2_equal2.grid(column=1,row=2,sticky='nw',pady=5,padx=3)
    accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2_labelframe2_combobox2 = ttk.Combobox(accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2_labelframe2,state='readonly',font = (custom_font,20),values= ['',"blue", "green", "red", "cyan", "magenta", "yellow", "black", "orange","purple", "brown", "pink", "gray", "olive", "teal", "navy"])
    accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2_labelframe2_combobox2.grid(column=2,row=2,sticky='nsew',pady=5,padx=[0,5])

    accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2_labelframe2_label3 = Label(accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2_labelframe2, text='Account Type', background=sub_lightdark, fg=text_color,font=('monogram',20))
    accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2_labelframe2_label3.grid(column=0,row=3,sticky='nw',pady=5,padx=3)
    accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2_labelframe2_equal3 = Label(accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2_labelframe2, text=':', background=sub_lightdark, fg=text_color,font=('monogram',20))
    accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2_labelframe2_equal3.grid(column=1,row=3,sticky='nw',pady=5,padx=3)
    accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2_labelframe2_combobox3 = ttk.Combobox(accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2_labelframe2,state='readonly',font = (custom_font,20),values=['','assets','liabilities','equity','revenue','expenses'])
    accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2_labelframe2_combobox3.grid(column=2,row=3,sticky='nsew',pady=5,padx=[0,5])

    accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2_labelframe2_label4 = Label(accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2_labelframe2, text='Account', background=sub_lightdark, fg=text_color,font=('monogram',20))
    accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2_labelframe2_label4.grid(column=0,row=4,sticky='nw',pady=5,padx=3)
    accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2_labelframe2_equal4 = Label(accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2_labelframe2, text=':', background=sub_lightdark, fg=text_color,font=('monogram',20))
    accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2_labelframe2_equal4.grid(column=1,row=4,sticky='nw',pady=5,padx=3)
    accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2_labelframe2_combobox4 = ttk.Combobox(accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2_labelframe2,state='readonly',font = (custom_font,20))
    accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2_labelframe2_combobox3.bind('<<ComboboxSelected>>', lambda event: [set_custom_combobox_value(accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2_labelframe2_combobox4,accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2_labelframe2_combobox3,False),accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2_labelframe2_combobox4.set('')])
    accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2_labelframe2_combobox4.bind('<FocusIn>', lambda event: set_custom_combobox_value(accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2_labelframe2_combobox4,accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2_labelframe2_combobox3,True))
    accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2_labelframe2_combobox4.grid(column=2,row=4,sticky='nsew',pady=5,padx=[0,5])

    accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2_frame1 = Frame(accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2,background=sub_lightdark)
    accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2_frame1.grid_columnconfigure([0,1],weight=1,uniform='a')
    accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2_frame1.grid(column=0,row=2,sticky='nsew')

    accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2_frame1_button1 = Button(accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2_frame1,text='Plot Graph',background=light_dark,fg=text_color,font=(custom_font,20), command = graph_plotting)
    accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2_frame1_button1.grid(column=1,row=0,sticky='nsew')

    accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2_frame1_button2 = Button(accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2_frame1,text='Clear Graph',background=light_dark,fg=text_color,font=(custom_font,20), command = clear_graph_plot)
    accountingpage_subframe2_frame3_categorypage_rightframe_frame1_frame2_frame1_button2.grid(column=0,row=0,sticky='nsew')

    return accountingpage_subframe2_frame3_categorypage_leftframe_frame1_treeview, accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame1_labelframe1_label4, accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame1_labelframe1_label2
def build_accounting_page_budget(master):
    def set_custom_combobox_value(widget,fetched_widget,setup):
        if not setup:
            widget.set('')
        value = fetched_widget.get()
        if len(value) > 0:
            placed_value = api.offline_fetch_account_from_type(value)
            widget.configure(values=[''] + placed_value)
    def calculated_Budget(event):
        duration = accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_combobox3.get()
        value = accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_entry1.get()

        try:
            value = float(value)
        except ValueError:
            accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_label5.configure(text=0)
            accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_label6.configure(text=0)
            accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_label7.configure(text=0)
            accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_label8.configure(text=0)
            return

        if duration not in ['daily', 'monthly', 'yearly','weekly']:
            accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_label5.configure(text=0)
            accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_label6.configure(text=0)
            accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_label7.configure(text=0)
            accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_label8.configure(text=0)
            return
        calculate_dict = {
        'daily' : [1,30.44,365],
        'monthly' : [0.03284,1,12],
        'yearly' : [0.00274,0.0833,1],
        'weekly' : [0.143,4.35,52.14]
        }   

        accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_label5.configure(text=f'{int(float(value) * calculate_dict[duration][0])}')
        accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_label6.configure(text=f'{int(float(value) * calculate_dict[duration][1])}')
        accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_label7.configure(text=f'{int(float(value) * calculate_dict[duration][2])}')
        accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_label8.configure(text=f'{int(float(value) * calculate_dict[duration][0] * 7)}')
    def reset_button_page():
        accountingpage_subframe2_frame4_canvas_frame1_frame1_treeview1.unbind('<<TreeviewSelect>>')
        accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2.pack_forget()
        accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame1.pack_forget()
        accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame3.pack_forget()
        accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_combobox1.configure(state='readonly')
        accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_combobox1.set('')
        accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_combobox2.configure(state='readonly',values=[])
        accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_combobox2.set('')
        accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_combobox3.configure(state='readonly')
        accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_combobox3.set('')
        accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_entry1.delete(0,END)
        accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_entry1.configure(fg=sub_textcolor,state='normal')
        accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_entry1.insert(0,'\u200BEnter Here')
        accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_label5.configure(text='0')
        accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_label6.configure(text='0')
        accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_label7.configure(text='0')
        accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_label8.configure(text='0')
        accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_frame1_button2.configure(text='')
        accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_frame1_button1.configure(command=back_button)

    def graph_and_table_plotting(search=False):
        day = accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe4_frame1_combobox1.get()
        month = accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe4_frame1_combobox2.get()
        year = accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe4_frame1_combobox3.get()

        if len(accountingpage_subframe2_frame4_canvas_frame1_frame1_treeview1.get_children()) < 1:
            ax1.clear()
            ax2.clear()
            ax1.pie([100], labels=['None'],textprops={'fontsize': 37},autopct='%1.1f%%',colors=['gray'])
            ax2.pie([100], labels=['None'],textprops={'fontsize': 37},autopct='%1.1f%%',colors=['gray'])

            graph1.draw_idle()
            graph2.draw_idle()

            accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe4_label3.configure(text='0')
            accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe4_label4.configure(text='0')
            accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe4_label5.configure(text='0%')
            return

        if day == '' and month == '' and year == '':
            if not search:
                for i in accountingpage_subframe2_frame4_canvas_frame1_frame1_treeview1.get_children():
                    accountingpage_subframe2_frame4_canvas_frame1_frame1_treeview1.delete(i)
                res = api.offline_budget_fetch()
                for i in res:
                    accountingpage_subframe2_frame4_canvas_frame1_frame1_treeview1.insert('','end',values=i)

                ax1.clear()
                ax2.clear()
                ax1.pie([100], labels=['None'],textprops={'fontsize': 37},autopct='%1.1f%%',colors=['gray'])
                ax2.pie([100], labels=['None'],textprops={'fontsize': 37},autopct='%1.1f%%',colors=['gray'])

                graph1.draw_idle()
                graph2.draw_idle()

                accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe4_label3.configure(text='0')
                accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe4_label4.configure(text='0')
                accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe4_label5.configure(text='0%')
                return
            else:
                search_list=[]
                for i in accountingpage_subframe2_frame4_canvas_frame1_frame1_treeview1.get_children():
                    search_list.append(accountingpage_subframe2_frame4_canvas_frame1_frame1_treeview1.item(i,'values')[3])
                    accountingpage_subframe2_frame4_canvas_frame1_frame1_treeview1.delete(i)
                placeholders = ','.join(['?'] * len(search_list))
                res = api.offline_budget_fetch(special_add_command=f' AND account IN ({placeholders})',data=search_list)
                for i in res:
                    accountingpage_subframe2_frame4_canvas_frame1_frame1_treeview1.insert('','end',values=i)
                ax1.clear()
                ax2.clear()
                ax1.pie([100], labels=['None'],textprops={'fontsize': 37},autopct='%1.1f%%',colors=['gray'])
                ax2.pie([100], labels=['None'],textprops={'fontsize': 37},autopct='%1.1f%%',colors=['gray'])

                graph1.draw_idle()
                graph2.draw_idle()

                accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe4_label3.configure(text='0')
                accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe4_label4.configure(text='0')
                accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe4_label5.configure(text='0%')
                return

                
        date = [day,month,year]
        temp_row = []
        for i in accountingpage_subframe2_frame4_canvas_frame1_frame1_treeview1.get_children():
            temp_row.append(accountingpage_subframe2_frame4_canvas_frame1_frame1_treeview1.item(i,'values'))
            accountingpage_subframe2_frame4_canvas_frame1_frame1_treeview1.delete(i)

        status, graph_list, table_list = api.offline_budget_graph_calc(temp_row,date)
        if status:
            for index,value in enumerate(table_list):
                accountingpage_subframe2_frame4_canvas_frame1_frame1_treeview1.insert('','end',values=((index+1,) + tuple(value[1:])))


            actual_values = [float(x) for x in graph_list[0]] if graph_list[0] else []
            budget_values = [float(x) for x in graph_list[2]] if graph_list[2] else []

            actual_data_tot = sum(actual_values)
            budget_data_tot = sum(budget_values)
            budget_remaining = budget_data_tot - actual_data_tot

            ax1.clear()
            ax2.clear()
            ax1.pie(graph_list[2], labels=graph_list[1],textprops={'fontsize': 37},autopct='%1.1f%%')
            ax2.pie(graph_list[0]+([budget_remaining] if budget_remaining >= 0 else [0]),labels=graph_list[3]+(['Amount Left'] if budget_remaining >= 0 else ['Amount Left']),textprops={'fontsize': 37},autopct='%1.1f%%')
            graph1.draw()
            graph2.draw()

            accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe4_label3.configure(text= str(budget_data_tot))
            accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe4_label4.configure(text = str(actual_data_tot))
            percentage_diff = str((actual_data_tot / budget_data_tot) * 100)[:6]
            accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe4_label5.configure(text=f'{percentage_diff}%')
    def treeview_select(lock = str in  ['remove','edit']):
        treeview_select = accountingpage_subframe2_frame4_canvas_frame1_frame1_treeview1.focus()
        state.treeview_selected_row_budget = treeview_select

        if treeview_select:
            accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame3.pack_forget()
            accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2.pack(side='top',fill='both',expand=1)
            values = accountingpage_subframe2_frame4_canvas_frame1_frame1_treeview1.item(treeview_select,'values')
            accountingpage_subframe2_frame4_canvas_frame1_frame1_treeview1.unbind('<<TreeviewSelect>>')
            accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_combobox1.set(values[2])
            accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_combobox2.set(values[3])
            accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_combobox3.set(values[4])
            accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_entry1.delete(0,END)
            accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_entry1.configure(fg=text_color)
            accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_entry1.insert(0,str(values[5]))
            calculated_Budget('hi')

            if lock == 'remove':
                accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_combobox1.configure(state='disabled')
                accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_combobox2.configure(state='disabled')
                accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_combobox3.configure(state='disabled')
                accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_entry1.configure(state='disabled')

            elif lock == 'edit':
                accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_combobox1.configure(state='disabled')
                accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_combobox2.configure(state='disabled')
            else:
                accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_combobox1.configure(state='readonly')
                accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_combobox2.configure(state='readonly')
                accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_combobox3.configure(state='readonly')
                accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_entry1.configure(state='normal')

    def back_button():
        reset_button_page()
        accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3.configure(text='Explanation')
        accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame1.pack(side='top',fill='both',expand=1)
    def to_button_page(type_of_command = str in ['add','remove','edit','search']):
        if getattr(state,'is_online') == False:
            accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3.configure(text='Configuration')
            if type_of_command == 'add':
                reset_button_page()
                accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame1.pack_forget()
                accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2.pack(side='top',fill='both',expand=1)
                accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_frame1_button2.configure(text='Add',command=lambda: button_command('add'))
                pass

            if type_of_command == 'remove':
                reset_button_page()
                accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame3.pack(side='top',fill='both',expand=1)
                accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_frame1_button2.configure(text='Remove',command=lambda: button_command('remove'))
                accountingpage_subframe2_frame4_canvas_frame1_frame1_treeview1.bind('<<TreeviewSelect>>',lambda e: treeview_select('remove'))
                accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_frame1_button1.configure(command=lambda:to_button_page('remove'))
                pass

            if type_of_command == 'edit':
                reset_button_page()
                accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame3.pack(side='top',fill='both',expand=1)
                accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_frame1_button2.configure(text='Edit',command=lambda: button_command('edit'))
                accountingpage_subframe2_frame4_canvas_frame1_frame1_treeview1.bind('<<TreeviewSelect>>',lambda e: treeview_select('edit'))
                accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_frame1_button1.configure(command=lambda:to_button_page('edit'))
                pass

            if type_of_command == 'search':
                reset_button_page()
                accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame1.pack_forget()
                accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2.pack(side='top',fill='both',expand=1)
                accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_frame1_button2.configure(text='Search',command=lambda: button_command('search'))
                pass
    def button_command(type_of_command = str in ['add','remove','edit','search']):
        if getattr(state,'is_online') == False:
            if type_of_command == 'add':
                status, res = api.offline_budget_add(accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_combobox1,
                                       accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_combobox2,
                                       accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_combobox3,
                                       accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_entry1,
                                       accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_label1)
                if status:
                    index = len(accountingpage_subframe2_frame4_canvas_frame1_frame1_treeview1.get_children())
                    accountingpage_subframe2_frame4_canvas_frame1_frame1_treeview1.insert('','end',values=[index+1,*res,0,0])
                    graph_and_table_plotting()
                    to_button_page('add')
                
                
            if type_of_command == 'remove':
                status = api.offline_budget_remove(accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_combobox1,
                                       accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_combobox2,
                                       accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_combobox3,
                                       accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_entry1,
                                       accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_label1)
                if status == True:
                    to_button_page('remove')
                    temp_list = []
                    for items in accountingpage_subframe2_frame4_canvas_frame1_frame1_treeview1.get_children():
                            if items != state.treeview_selected_row_budget:
                                temp_list.append(accountingpage_subframe2_frame4_canvas_frame1_frame1_treeview1.item(items,'values'))
                            accountingpage_subframe2_frame4_canvas_frame1_frame1_treeview1.delete(items)

                    for i,value in enumerate(temp_list):
                        edited_list = list(value[1:])
                        accountingpage_subframe2_frame4_canvas_frame1_frame1_treeview1.insert('','end',values=[i+1]+edited_list)

                    graph_and_table_plotting()


            if type_of_command == 'edit':
                status, new_list = api.offline_budget_edit(accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_combobox1,
                                       accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_combobox2,
                                       accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_combobox3,
                                       accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_entry1,
                                       accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_label1)
                if status:
                    to_button_page('edit')
                    new_list = ['3'] + new_list + ['0','0']
                    accountingpage_subframe2_frame4_canvas_frame1_frame1_treeview1.item(state.treeview_selected_row_budget,values=new_list)
                    graph_and_table_plotting()


            if type_of_command == 'search':
                status, new_list = api.offline_budget_search(accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_combobox1,
                                       accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_combobox2,
                                       accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_combobox3,
                                       accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_entry1,
                                       accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_label1)
                if status:
                    for row in accountingpage_subframe2_frame4_canvas_frame1_frame1_treeview1.get_children():
                        accountingpage_subframe2_frame4_canvas_frame1_frame1_treeview1.delete(row)

                    for value in new_list:
                        value = ['3'] + list(value) + ['0','0']
                        accountingpage_subframe2_frame4_canvas_frame1_frame1_treeview1.insert('','end',values=value)
                    graph_and_table_plotting(search=True)
                    reset_button_page()
                    to_button_page('search')


    master.grid_rowconfigure(0,weight=1)
    master.grid_columnconfigure(0,weight=1)

    #First Frame Budget
    accountingpage_subframe2_frame4_canvas_frame1 = Frame(master, background='red')
    accountingpage_subframe2_frame4_canvas_frame1.grid(column=0,row=0,sticky='nsew')
    accountingpage_subframe2_frame4_canvas_frame1.grid_propagate(False)
    accountingpage_subframe2_frame4_canvas_frame1.grid_columnconfigure(0,weight=1)
    accountingpage_subframe2_frame4_canvas_frame1.grid_rowconfigure(0,weight=1)

    #SUB FRAME FIRST FRAME
    accountingpage_subframe2_frame4_canvas_frame1_frame1 = Frame(accountingpage_subframe2_frame4_canvas_frame1,background=sub_lightdark)
    accountingpage_subframe2_frame4_canvas_frame1_frame1.grid(column=0,row=0,sticky='nsew')
    accountingpage_subframe2_frame4_canvas_frame1_frame1.grid_columnconfigure(0,weight=1)
    accountingpage_subframe2_frame4_canvas_frame1_frame1.grid_rowconfigure(0,weight=1)

    accountingpage_subframe2_frame4_canvas_frame1_frame1_scrollbar = ttk.Scrollbar(accountingpage_subframe2_frame4_canvas_frame1_frame1)
    accountingpage_subframe2_frame4_canvas_frame1_frame1_scrollbar.grid(column=1,row=0,sticky='nsew')

    headings = ('No.','ID','Type','Account','Duration','Budget Value', 'Actual Value', 'Difference')

    accountingpage_subframe2_frame4_canvas_frame1_frame1_treeview1 = ttk.Treeview(accountingpage_subframe2_frame4_canvas_frame1_frame1,columns=headings, show='headings',yscrollcommand=accountingpage_subframe2_frame4_canvas_frame1_frame1_scrollbar)
    accountingpage_subframe2_frame4_canvas_frame1_frame1_treeview1.grid(column=0,row=0,sticky='nsew')
    accountingpage_subframe2_frame4_canvas_frame1_frame1_scrollbar.configure(command=accountingpage_subframe2_frame4_canvas_frame1_frame1_treeview1.yview)

    accountingpage_subframe2_frame4_canvas_frame1_frame1_treeview1.column('No.',anchor='w',stretch=True,minwidth=20,width=20)
    accountingpage_subframe2_frame4_canvas_frame1_frame1_treeview1.heading('No.',text='No.')

    accountingpage_subframe2_frame4_canvas_frame1_frame1_treeview1.column('ID',anchor='w',stretch=True,minwidth=20,width=20)
    accountingpage_subframe2_frame4_canvas_frame1_frame1_treeview1.heading('ID',text='ID')

    accountingpage_subframe2_frame4_canvas_frame1_frame1_treeview1.column('Type',anchor='w',stretch=True,minwidth=80,width=80)
    accountingpage_subframe2_frame4_canvas_frame1_frame1_treeview1.heading('Type',text='Type')

    accountingpage_subframe2_frame4_canvas_frame1_frame1_treeview1.column('Account',anchor='w',stretch=True,minwidth=80,width=80)
    accountingpage_subframe2_frame4_canvas_frame1_frame1_treeview1.heading('Account',text='Account')

    accountingpage_subframe2_frame4_canvas_frame1_frame1_treeview1.column('Duration',anchor='w',stretch=True,minwidth=80,width=80)
    accountingpage_subframe2_frame4_canvas_frame1_frame1_treeview1.heading('Duration',text='Duration')

    accountingpage_subframe2_frame4_canvas_frame1_frame1_treeview1.column('Budget Value',anchor='w',stretch=True,minwidth=100,width=100)
    accountingpage_subframe2_frame4_canvas_frame1_frame1_treeview1.heading('Budget Value',text='Budget Value')

    accountingpage_subframe2_frame4_canvas_frame1_frame1_treeview1.column('Actual Value',anchor='w',stretch=True,minwidth=100,width=100)
    accountingpage_subframe2_frame4_canvas_frame1_frame1_treeview1.heading('Actual Value',text='Actual Value')

    accountingpage_subframe2_frame4_canvas_frame1_frame1_treeview1.column('Difference',anchor='w',stretch=True,minwidth=100,width=100)
    accountingpage_subframe2_frame4_canvas_frame1_frame1_treeview1.heading('Difference',text='Difference')

    #Frame 1 
    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1 = Frame(accountingpage_subframe2_frame4_canvas_frame1_frame1,background=light_dark)
    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1.grid(column=0,row=1,sticky='nsew',pady=[5,0],columnspan=2)
    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1.grid_columnconfigure(0,weight=1)
    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1.grid_rowconfigure(1,weight=1)

    #Frame 1 Message Frame
    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame1 = Frame(accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1,background=sub_lightdark)
    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame1.grid(column=0,row=0,sticky='nsew',padx=3,pady=3)

    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_label1 = Label(accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame1,fg=error_color,background=sub_lightdark,font=(custom_font,20),text='')
    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_label1.pack(side='left')

    #FRAME 1 BUTTON FRAME
    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2 = Frame(accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1,background=sub_lightdark, height=380)
    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2.grid_propagate(False)
    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2.grid_columnconfigure(2,weight=1)
    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2.grid_rowconfigure([0,1],weight=1,uniform='a')
    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2.grid(column=0,row=1,sticky='nsew',padx=3,pady=[0,3])

    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe1 = LabelFrame(accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2,background=sub_lightdark,text='Budget Data',font=(custom_font,20,'bold'),fg=text_color)
    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe1.grid(column=0,row=0,sticky='nsew',padx=3)

    fig1 = Figure(figsize=(8,5),dpi=30)
    fig1.patch.set_facecolor(color=sub_lightdark)
    ax1 = fig1.add_axes([0,0,1,1])

    ax1.set_aspect("equal")
    ax1.set_xticks([])
    ax1.set_yticks([])
    for spine in ax1.spines.values():
        spine.set_visible(False)

    # Optional: set limits so the blank axes look circular
    ax1.set_xlim(-1, 1)
    ax1.set_ylim(-1, 1)

    ax1.pie([100], labels=['None'],textprops={'fontsize': 37},autopct='%1.1f%%',colors=['gray'])

    graph1 = FigureCanvasTkAgg(fig1,accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe1)
    graph1.get_tk_widget().pack(side='top',expand=1,fill='both',padx=5,pady=[0,8])

    #Actual Graph Labelframe2
    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe2 = LabelFrame(accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2,background=sub_lightdark,text='Actual Data',font=(custom_font,20,'bold'),fg=text_color)
    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe2.grid(column=1,row=0,sticky='nsew',padx=[0,3])

    fig2 = Figure(figsize=(8,5),dpi=30)
    fig2.patch.set_facecolor(color=sub_lightdark)
    ax2 = fig2.add_axes([0,0,1,1])

    ax2.set_aspect("equal")
    ax2.set_xticks([])
    ax2.set_yticks([])
    for spine in ax2.spines.values():
        spine.set_visible(False)

    # Optional: set limits so the blank axes look circular
    ax2.set_xlim(-1, 1)
    ax2.set_ylim(-1, 1)

    labels = 'Frogs', 'Hogs', 'Dogs', 'Logs'
    sizes = [15, 30, 45, 10]

    ax2.pie(sizes, labels=labels,textprops={'fontsize': 37},autopct='%1.1f%%')

    graph2 = FigureCanvasTkAgg(fig2,accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe2)
    graph2.get_tk_widget().pack(side='top',expand=1,fill='both',padx=5,pady=[0,8])

    #Input Frame
    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3 = LabelFrame(accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2,background=sub_lightdark,text='Explanation',font=(custom_font,20,'bold'),fg=text_color)
    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3.grid(column=2,row=0,sticky='nsew',padx=3,rowspan=2,pady=[0,5])

    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame1 = Frame(accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3,background=sub_lightdark)

    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame1_label1 = Label(accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame1, text=' - Use Date to see budget status', background=sub_lightdark, fg=text_color,font=('monogram',20))
    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame1_label1.grid(column=0,row=0,sticky='nsw',pady=[5,0])

    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame1_label1 = Label(accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame1, text=' - In order to show data in table / graph\n   use SEARCH', background=sub_lightdark, fg=text_color,font=('monogram',20),justify='left')
    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame1_label1.grid(column=0,row=1,sticky='nsw',pady=[5,0])

    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame1_label1 = Label(accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame1, text=' - Budget isnt based of actual Revenue!', background=sub_lightdark, fg=text_color,font=('monogram',20),justify='left')
    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame1_label1.grid(column=0,row=2,sticky='nsw',pady=[5,0])

    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame1_label1 = Label(accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame1, text=' - In order to see individual calculated\n   Budget use EDIT ', background=sub_lightdark, fg=text_color,font=('monogram',20),justify='left')
    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame1_label1.grid(column=0,row=3,sticky='nsw',pady=[5,0])

    #treeview select frame
    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame3 = Frame(accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3,background=sub_lightdark)
    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame3.grid_columnconfigure(0,weight=1)
    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame3.grid_rowconfigure(0,weight=1)
    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame3.pack(side='top',fill='both',expand=1)

    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame3_label = Label(accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame3, text='Please click on the row\n you want to change', background=sub_lightdark, fg=text_color,font=('monogram',20))
    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame3_label.grid(column=0,row=0,sticky='nsew')

    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame3_button = Button(accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame3,text='Back',foreground=text_color,background=light_dark,font=(custom_font,20,'bold'),command=back_button)
    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame3_button.grid(column=0,row=1,sticky='nsew')

    #Frame
    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2 = Frame(accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3,background=sub_lightdark)
    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2.grid_columnconfigure(2,weight=1)
    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2.grid_rowconfigure(8,weight=1)
    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2

    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_label1 = Label(accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2, text='Account Type', background=sub_lightdark, fg=text_color,font=('monogram',20))
    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_label1.grid(column=0,row=0,sticky='nw',pady=5,padx=[3,0])
    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_equal1 = Label(accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2, text=':', background=sub_lightdark, fg=text_color,font=('monogram',20))
    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_equal1.grid(column=1,row=0,sticky='nw',pady=5)
    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_combobox1 = ttk.Combobox(accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2, background = light_dark, foreground = text_color,font=('monogram',20),state='readonly',justify='left', values = ['liabilities','equity','expenses'])
    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_combobox1.grid(column=2,row=0,sticky='new',pady=5,padx=[0,5])
    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_combobox1.bind('<<ComboboxSelected>>', lambda event: [set_custom_combobox_value(accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_combobox2,accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_combobox1,False),accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_combobox2.set('')])

    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_label2 = Label(accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2, text='Account', background=sub_lightdark, fg=text_color,font=('monogram',20))
    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_label2.grid(column=0,row=1,sticky='nw',pady=5,padx=[3,0])
    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_equal2 = Label(accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2, text=':', background=sub_lightdark, fg=text_color,font=('monogram',20))
    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_equal2.grid(column=1,row=1,sticky='nw',pady=5)
    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_combobox2 = ttk.Combobox(accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2, background = light_dark, foreground = text_color,font=('monogram',20),state='readonly',justify='left')
    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_combobox2.grid(column=2,row=1,sticky='new',pady=5,padx=[0,5])

    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_label3 = Label(accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2, text='Budget Duration', background=sub_lightdark, fg=text_color,font=('monogram',20))
    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_label3.grid(column=0,row=2,sticky='nw',pady=5,padx=[3,0])
    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_equal3 = Label(accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2, text=':', background=sub_lightdark, fg=text_color,font=('monogram',20))
    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_equal3.grid(column=1,row=2,sticky='nw',pady=5)
    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_combobox3 = ttk.Combobox(accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2, background = light_dark, foreground = text_color,font=('monogram',20),state='readonly',justify='left', values= ['daily','weekly','monthly','yearly'])
    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_combobox3.grid(column=2,row=2,sticky='new',pady=5,padx=[0,5])
    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_combobox3.bind('<<ComboboxSelected>>', calculated_Budget)

    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_label4 = Label(accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2, text='Budget Value', background=sub_lightdark, fg=text_color,font=('monogram',20))
    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_label4.grid(column=0,row=3,sticky='nw',pady=5,padx=[3,0])
    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_equal4 = Label(accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2, text=':', background=sub_lightdark, fg=text_color,font=('monogram',20))
    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_equal4.grid(column=1,row=3,sticky='nw',pady=5)
    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_entry1 = Entry(accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2, background = light_dark, fg = sub_textcolor,font=('monogram',20),disabledbackground=light_dark,disabledforeground=text_color)
    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_entry1.insert(0,'\u200BEnter Here')
    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_entry1.bind('<FocusIn>', lambda event: entry_text(accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_entry1,['\u200BEnter Here']))
    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_entry1.bind('<FocusOut>', lambda event: entry_text(accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_entry1,['\u200BEnter Here'],True,'\u200BEnter Here'))
    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_entry1.bind('<KeyRelease>',calculated_Budget )
    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_entry1.grid(column=2,row=3,sticky='new',pady=5,padx=[0,5])

    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_label5 = Label(accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2, text='Calculated Daily Budget', background=sub_lightdark, fg=text_color,font=('monogram',20))
    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_label5.grid(column=0,row=4,sticky='nw',pady=5,padx=[3,0])
    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_equal5 = Label(accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2, text=':', background=sub_lightdark, fg=text_color,font=('monogram',20))
    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_equal5.grid(column=1,row=4,sticky='nw',pady=5)
    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_label5 = Label(accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2, text='0', background=sub_lightdark, fg=text_color,font=('monogram',20,'bold'))
    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_label5.grid(column=2,row=4,sticky='nw',pady=5,padx=[3,0])

    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_label6 = Label(accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2, text='Calculated Monthly Budget', background=sub_lightdark, fg=text_color,font=('monogram',20))
    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_label6.grid(column=0,row=6,sticky='nw',pady=5,padx=[3,0])
    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_equal6 = Label(accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2, text=':', background=sub_lightdark, fg=text_color,font=('monogram',20))
    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_equal6.grid(column=1,row=6,sticky='nw',pady=5)
    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_label6 = Label(accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2, text='0', background=sub_lightdark, fg=text_color,font=('monogram',20,'bold'))
    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_label6.grid(column=2,row=6,sticky='nw',pady=5,padx=[3,0])

    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_label7 = Label(accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2, text='Calculated Yearly Budget', background=sub_lightdark, fg=text_color,font=('monogram',20))
    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_label7.grid(column=0,row=7,sticky='nw',pady=5,padx=[3,0])
    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_equal7 = Label(accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2, text=':', background=sub_lightdark, fg=text_color,font=('monogram',20))
    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_equal7.grid(column=1,row=7,sticky='nw',pady=5)
    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_label7 = Label(accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2, text='0', background=sub_lightdark, fg=text_color,font=('monogram',20,'bold'))
    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_label7.grid(column=2,row=7,sticky='nw',pady=5,padx=[3,0])

    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_label8 = Label(accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2, text='Calculated Weekly Budget', background=sub_lightdark, fg=text_color,font=('monogram',20))
    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_label8.grid(column=0,row=5,sticky='nw',pady=5,padx=[3,0])
    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_equal8 = Label(accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2, text=':', background=sub_lightdark, fg=text_color,font=('monogram',20))
    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_equal8.grid(column=1,row=5,sticky='nw',pady=5)
    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_label8 = Label(accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2, text='0', background=sub_lightdark, fg=text_color,font=('monogram',20,'bold'))
    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_label8.grid(column=2,row=5,sticky='nw',pady=5,padx=[3,0])

    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_frame1 = Frame(accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2,background='white')
    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_frame1.grid_columnconfigure([0,1],weight=1,uniform='a')
    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_frame1.grid(column=0,row=8,sticky='sew',columnspan=3)

    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_frame1_button1 = Button(accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_frame1,text='Back',foreground=text_color,background=light_dark,font=(custom_font,20,'bold'),command=back_button)
    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_frame1_button1.grid(column=0,row=0,sticky='nsew')

    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_frame1_button2 = Button(accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_frame1,text='Confirm',foreground=text_color,background=light_dark,font=(custom_font,20,'bold'))
    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2_frame1_button2.grid(column=1,row=0,sticky='nsew')

    #Button Frame
    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_frame1 = Frame(accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2,background=light_dark)
    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_frame1.grid_columnconfigure(0,weight=1)
    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_frame1.grid_rowconfigure([0,1,2,3],weight=1, uniform='a')
    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_frame1.grid(column=3,row=0,sticky='nsew',rowspan=2)

    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_frame1_button1 = Button(accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_frame1,text='Add',foreground=text_color,background=light_dark,font=(custom_font,20,'bold'),command=lambda:to_button_page('add'))
    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_frame1_button1.grid(column=0,row=0,sticky='nsew',padx=3,ipadx=30)

    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_frame1_button2 = Button(accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_frame1,text='Remove',foreground=text_color,background=light_dark,font=(custom_font,20,'bold'),command=lambda:to_button_page('remove'))
    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_frame1_button2.grid(column=0,row=1,sticky='nsew',padx=3,ipadx=30)

    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_frame1_button3 = Button(accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_frame1,text='Edit',foreground=text_color,background=light_dark,font=(custom_font,20,'bold'),command=lambda:to_button_page('edit'))
    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_frame1_button3.grid(column=0,row=2,sticky='nsew',padx=3,ipadx=30)

    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_frame1_button4 = Button(accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_frame1,text='Search',foreground=text_color,background=light_dark,font=(custom_font,20,'bold'),command=lambda:to_button_page('search'))
    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_frame1_button4.grid(column=0,row=3,sticky='nsew',padx=3,ipadx=30)


    #lABEL FRAME GRAPHS
    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe4 = LabelFrame(accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2,background=sub_lightdark,text='Graph and Table data',font=(custom_font,20,'bold'),fg=text_color)
    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe4.grid_columnconfigure(2,weight=1)
    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe4.grid(column=0,row=1,sticky='nsew',padx=3,rowspan=2,columnspan=2,pady=[0,5])

    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe4_label1 = Label(accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe4, text='Date', background=sub_lightdark, fg=text_color,font=('monogram',20))
    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe4_label1.grid(column=0,row=0,sticky='nw',pady=5,padx=[3,0])
    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe4_equal1 = Label(accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe4, text=':', background=sub_lightdark, fg=text_color,font=('monogram',20))
    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe4_equal1.grid(column=1,row=0,sticky='nw',pady=5)
    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe4_frame1 = Frame(accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe4,background=sub_lightdark)
    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe4_frame1.grid(column=2,row=0,sticky='nw',pady=5,padx=[3,0])
    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe4_frame1_combobox1 = ttk.Combobox(accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe4_frame1, background = light_dark, foreground = text_color,font=('monogram',20),state='readonly',justify='left',width=5)
    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe4_frame1_combobox1.pack(side='left')
    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe4_frame1_combobox2 = ttk.Combobox(accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe4_frame1, background = light_dark, foreground = text_color,font=('monogram',20),state='readonly',justify='left',width=5)
    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe4_frame1_combobox2.pack(side='left',padx=5)
    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe4_frame1_combobox3 = ttk.Combobox(accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe4_frame1, background = light_dark, foreground = text_color,font=('monogram',20),state='readonly',justify='left',width=7)
    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe4_frame1_combobox3.pack(side='left')
    combobox_date_set_year(accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe4_frame1_combobox3)
    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe4_frame1_combobox3.bind('<<ComboboxSelected>>', lambda e: [combobox_date(accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe4_frame1_combobox1,accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe4_frame1_combobox2,accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe4_frame1_combobox3,select='year'),graph_and_table_plotting()])
    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe4_frame1_combobox2.bind('<<ComboboxSelected>>', lambda e: [combobox_date(accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe4_frame1_combobox1,accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe4_frame1_combobox2,accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe4_frame1_combobox3,select='month'),graph_and_table_plotting()])
    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe4_frame1_combobox1.bind('<<ComboboxSelected>>',lambda e: graph_and_table_plotting())

    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe4_label2 = Label(accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe4, text='Budget Total', background=sub_lightdark, fg=text_color,font=('monogram',20))
    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe4_label2.grid(column=0,row=1,sticky='nw',pady=5,padx=[3,0])
    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe4_equal2 = Label(accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe4, text=':', background=sub_lightdark, fg=text_color,font=('monogram',20))
    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe4_equal2.grid(column=1,row=1,sticky='nw',pady=5)
    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe4_label3 = Label(accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe4, text='0918182', background=sub_lightdark, fg=text_color,font=('monogram',20,'bold'))
    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe4_label3.grid(column=2,row=1,sticky='nw',pady=5,padx=[3,0])

    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe4_label6 = Label(accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe4, text='Actual Total', background=sub_lightdark, fg=text_color,font=('monogram',20))
    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe4_label6.grid(column=0,row=2,sticky='nw',pady=5,padx=[3,0])
    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe4_equal3 = Label(accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe4, text=':', background=sub_lightdark, fg=text_color,font=('monogram',20))
    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe4_equal3.grid(column=1,row=2,sticky='nw',pady=5)
    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe4_label4 = Label(accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe4, text='0918182', background=sub_lightdark, fg=text_color,font=('monogram',20,'bold'))
    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe4_label4.grid(column=2,row=2,sticky='nw',pady=5,padx=[3,0])

    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe4_label7 = Label(accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe4, text='Difference Total', background=sub_lightdark, fg=text_color,font=('monogram',20))
    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe4_label7.grid(column=0,row=3,sticky='nw',pady=5,padx=[3,0])
    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe4_equal4 = Label(accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe4, text=':', background=sub_lightdark, fg=text_color,font=('monogram',20))
    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe4_equal4.grid(column=1,row=3,sticky='nw',pady=5)
    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe4_label5 = Label(accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe4, text='38%', background=sub_lightdark, fg=text_color,font=('monogram',20,'bold'))
    accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe4_label5.grid(column=2,row=3,sticky='nw',pady=5,padx=[3,0])

    return accountingpage_subframe2_frame4_canvas_frame1_frame1_treeview1,ax1,graph1,ax2,graph2,accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe4_label3,accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe4_label4,accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe4_label5,accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe4_frame1_combobox1,accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe4_frame1_combobox2,accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe4_frame1_combobox3,accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame1,accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame2,accountingpage_subframe2_frame4_canvas_frame1_frame1_frame1_frame2_labelframe3_frame3

#Functions to make life easier
def pack_center(master,widget,color):# exactly what it sounds to pack_center
    fill_pack1,fill_pack2, = Frame(master,background=color),Frame(master,background=color)
    fill_pack1.pack(side='top',expand=True,fill='both')
    widget.pack(side='top')
    fill_pack2.pack(side='top',expand=True,fill='both')
def load_page(page,auto_login_email=None,auto_login_password=None):# To load needed pages only not all
    loading_page.place(relx=0, rely=0, relwidth=1, relheight = 1)
        
    def do_switch():
        for p in page_built:
            frame = globals()[p]
            frame.pack_forget()
            if (p != page and p not in page_linked[page]) and page_built[p] == True:
                for widget in frame.winfo_children():
                    widget.destroy()
                page_built[p] = False

        if page_built[page] == False:
            if page_built[page] == False and auto_login_email and auto_login_password:
                globals()[f'build_{page}'](auto_login_email,auto_login_password)
                page_built[page] = True
                
            elif page_built[page]== False:
                globals()[f'build_{page}']()
                page_built[page] = True

        
        for p in page_linked[page]:
            if page_built[p] == False:
                globals()[f'build_{p}']()
                page_built[p] = True

        frame = globals()[page]
        frame.pack(fill='both', expand = True)
        window.update_idletasks()


        window.after(1000, lambda: loading_page.place_forget())

    window.after(100, do_switch)
def entry_text(widget=Widget,text_array=(),add=False, add_text=None,password=False):# Function to change entry
    text = widget.get()
    if add:
        if text == '':
            widget.insert(0, add_text)
            widget.configure(foreground = sub_textcolor,show = '')

    else:
        if text in text_array:
            widget.delete(0, END)
            widget.configure(foreground = text_color)
            if password:
                widget.configure(show='*')
def online_startup():
    setattr(state,'is_online',True)
    if path.exists('config.json') and path.isfile('config.json'):
        with open('config.json', 'r') as file:
            data = json.load(file)
            email = str(data.get('email'))
            password = str(data.get('password'))

        load_page('login_page',email,password)
    else:
        load_page('login_page')

def offline_startup():
    setattr(state,'is_online',False)
    connect = sql.connect('database.db')
    cursor = connect.cursor()
    cursor.execute('PRAGMA foreign_keys = ON')

    #type eg. Assets, Liabilities etc
    account_type_table = '''
    CREATE TABLE IF NOT EXISTS account_types (
    account_type TEXT PRIMARY KEY
    );
    '''
    cursor.execute(account_type_table)

    account_table = '''
    CREATE TABLE IF NOT EXISTS accounts (
    id INTEGER PRIMARY KEY,
    account_type TEXT NOT NULL,
    account TEXT UNIQUE,
    transaction_count INTEGER DEFAULT 0,
    actual_value FLOAT DEFAULT 0,
 
    FOREIGN KEY (account_type) REFERENCES account_types(account_type)
    );
    '''
    cursor.execute(account_table)

    budget_table = '''
    CREATE TABLE IF NOT EXISTS budget (
    id INTEGER PRIMARY KEY,
    account_type TEXT NOT NULL,
    account TEXT UNIQUE NOT NULL,
    duration TEXT NOT NULL CHECK(duration IN ('daily','monthly','yearly','weekly')),
    budget_value FLOAT NOT NULL,

    FOREIGN KEY (account) REFERENCES accounts(account) ON UPDATE CASCADE ON DELETE CASCADE
    FOREIGN KEY (account_type) REFERENCES account_types(account_type) ON UPDATE CASCADE ON DELETE CASCADE
    );
    '''
    cursor.execute(budget_table)

    daily_transaction_total = '''
    CREATE TABLE IF NOT EXISTS daily_total (
    id INTEGER PRIMARY KEY,
    account TEXT NOT NULL,
    account_type TEXT NOT NULL,
    day INTEGER NOT NULL,
    month INTEGER NOT NULL,
    year INTEGER NOT NULL,
    amount FLOAT DEFAULT 0,
    transaction_count INTEGER NOT NULL DEFAULT 0,
    UNIQUE(account, account_type, day, month, year),
    FOREIGN KEY (account) REFERENCES accounts(account) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (account_type) REFERENCES account_types(account_type) ON UPDATE CASCADE ON DELETE CASCADE
    );
    '''
    cursor.execute(daily_transaction_total)

    transaction_table = '''
    CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY,
    from_account_type TEXT NOT NULL,
    from_account TEXT NOT NULL,
    to_account_type TEXT NOT NULL,
    to_account TEXT NOT NULL,
    day INTEGER NOT NULL,
    month INTEGER NOT NULL,
    year INTEGER NOT NULL,
    description TEXT NOT NULL,
    amount FLOAT NOT NULL,  
    FOREIGN KEY (from_account_type) REFERENCES account_types(account_type) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (from_account) REFERENCES accounts(account) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (to_account_type) REFERENCES account_types(account_type) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (to_account) REFERENCES accounts(account) ON UPDATE CASCADE ON DELETE CASCADE
    );'''
    cursor.execute(transaction_table)
    connect.commit()

    #Trigger for adding count to count and actual value
    insert_trigger = '''
    CREATE TRIGGER IF NOT EXISTS update_summary_after_insert
    AFTER INSERT ON transactions
    BEGIN
        UPDATE accounts
        SET actual_value = actual_value +
            CASE
                WHEN NEW.from_account_type = 'assets'
                    AND NEW.to_account_type IN ('assets','expenses','liabilities','equity')
                    THEN -NEW.amount
                
                WHEN NEW.from_account_type = 'liabilities'
                    AND NEW.to_account_type IN ('liabilities','expenses','equity')
                    THEN -NEW.amount

                WHEN NEW.from_account_type = 'equity'
                    AND NEW.to_account_type IN ('assets','expenses')
                    THEN -NEW.amount
                
                ELSE NEW.amount
            END,
            transaction_count = transaction_count + 1

        WHERE account = NEW.from_account;

        UPDATE accounts
        SET actual_value = actual_value +
            CASE
                WHEN NEW.to_account_type = 'liabilities'
                    AND NEW.from_account_type = 'assets'
                    THEN -NEW.amount

                WHEN NEW.to_account_type = 'equity'
                    AND NEW.from_account_type IN ('assets','liabilities')
                    THEN -NEW.amount

                ELSE NEW.amount
            END,
            transaction_count = transaction_count + 
                CASE
                    WHEN NEW.to_account = NEW.from_account
                    THEN 0
                    ELSE 1
                END
        WHERE account = NEW.to_account;

        INSERT INTO daily_total (account,account_type,day,month,year,amount,transaction_count) VALUES (
            NEW.from_account,
            NEW.from_account_type,
            NEW.day,
            NEW.month,
            NEW.year,
            CASE
                WHEN NEW.from_account_type = 'assets'
                    AND NEW.to_account_type IN ('assets','expenses','liabilities','equity')
                    THEN -NEW.amount
                
                WHEN NEW.from_account_type = 'liabilities'
                    AND NEW.to_account_type IN ('liabilities','expenses','equity')
                    THEN -NEW.amount

                WHEN NEW.from_account_type = 'equity'
                    AND NEW.to_account_type IN ('assets','expenses')
                    THEN -NEW.amount
                
                ELSE NEW.amount
            END,
            1
            )
            ON CONFLICT(account,account_type, day, month,year)
            DO UPDATE SET amount = amount + EXCLUDED.amount,transaction_count = transaction_count + 
                CASE
                    WHEN NEW.to_account = NEW.from_account
                    THEN 0
                    ELSE 1
                END;

        INSERT INTO daily_total (account,account_type,day,month,year,amount,transaction_count) VALUES (
            NEW.to_account,
            NEW.to_account_type,
            NEW.day,
            NEW.month,
            NEW.year,
            CASE
                WHEN NEW.to_account_type = 'liabilities'
                    AND NEW.from_account_type = 'assets'
                    THEN -NEW.amount

                WHEN NEW.to_account_type = 'equity'
                    AND NEW.from_account_type IN ('assets','liabilities')
                    THEN -NEW.amount

                ELSE NEW.amount
            END,
            1
            )
            ON CONFLICT(account,account_type, day, month,year)
            DO UPDATE SET amount = amount + EXCLUDED.amount,transaction_count = transaction_count + 
                CASE
                    WHEN NEW.to_account = NEW.from_account
                    THEN 0
                    ELSE 1
                END;

    END;
    '''
    remove_trigger = '''
    CREATE TRIGGER IF NOT EXISTS update_summary_after_remove
    AFTER DELETE ON transactions
    BEGIN
        UPDATE accounts
        SET actual_value = actual_value -
            CASE
                WHEN OLD.from_account_type = 'assets'
                    AND OLD.to_account_type IN ('assets','expenses','liabilities','equity')
                    THEN -OLD.amount
                
                WHEN OLD.from_account_type = 'liabilities'
                    AND OLD.to_account_type IN ('liabilities','expenses','equity')
                    THEN -OLD.amount

                WHEN OLD.from_account_type = 'equity'
                    AND OLD.to_account_type IN ('assets','expenses')
                    THEN -OLD.amount
                
                ELSE OLD.amount
            END,
            transaction_count = transaction_count - 1
        WHERE account = OLD.from_account;

        UPDATE accounts
        SET actual_value = actual_value -
            CASE
                WHEN OLD.to_account_type = 'liabilities'
                    AND OLD.from_account_type = 'assets'
                    THEN -OLD.amount

                WHEN OLD.to_account_type = 'equity'
                    AND OLD.from_account_type IN ('assets','liabilities')
                    THEN -OLD.amount

                ELSE OLD.amount
            END,
            transaction_count = transaction_count - 
                        CASE
                            WHEN OLD.from_account = OLD.to_account 
                            THEN 0
                            ELSE 1
                        END
        WHERE account = OLD.to_account;

        INSERT INTO daily_total (account,account_type,day,month,year,amount,transaction_count) VALUES (
            OLD.from_account,
            OLD.from_account_type,
            OLD.day,
            OLD.month,
            OLD.year,
            CASE
                WHEN OLD.from_account_type = 'assets'
                    AND OLD.to_account_type IN ('assets','expenses','liabilities','equity')
                    THEN -OLD.amount
                
                WHEN OLD.from_account_type = 'liabilities'
                    AND OLD.to_account_type IN ('liabilities','expenses','equity')
                    THEN -OLD.amount

                WHEN OLD.from_account_type = 'equity'
                    AND OLD.to_account_type IN ('assets','expenses')
                    THEN -OLD.amount
                
                ELSE OLD.amount
            END,
            1
            )
            ON CONFLICT(account,account_type, day, month,year)
            DO UPDATE SET amount = amount - EXCLUDED.amount, transaction_count = transaction_count - 1;

        INSERT INTO daily_total (account,account_type,day,month,year,amount,transaction_count) VALUES (
            OLD.to_account,
            OLD.to_account_type,
            OLD.day,
            OLD.month,
            OLD.year,
            CASE
                WHEN OLD.to_account_type = 'liabilities'
                    AND OLD.from_account_type = 'assets'
                    THEN -OLD.amount

                WHEN OLD.to_account_type = 'equity'
                    AND OLD.from_account_type IN ('assets','liabilities')
                    THEN -OLD.amount

                ELSE OLD.amount
            END, 
            CASE
                WHEN OLD.to_account = OLD.from_account
                THEN 0
                ELSE 1
            END
            )
            ON CONFLICT(account,account_type, day, month,year)
            DO UPDATE SET amount = amount - EXCLUDED.amount, transaction_count = transaction_count - 
                            CASE
                                WHEN OLD.from_account = OLD.to_account 
                                THEN 0
                                ELSE 1
                            END;
        DELETE FROM daily_total WHERE amount = 0 AND transaction_count = 0;
        END;
        '''
    update_trigger = '''
    CREATE TRIGGER IF NOT EXISTS update_summary_after_update
    AFTER UPDATE ON transactions
    BEGIN
        UPDATE accounts
        set actual_value = actual_value - (
                CASE
                    WHEN OLD.from_account_type = 'assets'
                        AND OLD.to_account_type IN ('assets','expenses','liabilities','equity')
                        THEN -OLD.amount 

                    WHEN OLD.from_account_type = 'liabilities'
                        AND OLD.to_account_type IN ('liabilities','expenses','equity')
                        THEN -OLD.amount

                    WHEN OLD.from_account_type = 'equity'
                        AND OLD.to_account_type IN ('assets','expenses')
                        THEN -OLD.amount
                    
                    ELSE OLD.amount
                END
            ),
            transaction_count = transaction_count - 1
        WHERE account = OLD.from_account;

        UPDATE accounts
        SET actual_value = actual_value - (
                CASE
                    WHEN OLD.to_account_type = 'liabilities'
                        AND OLD.from_account_type = 'assets'
                        THEN -OLD.amount

                    WHEN OLD.to_account_type = 'equity'
                        AND OLD.from_account_type IN ('assets','liabilities')
                        THEN -OLD.amount

                    ELSE OLD.amount
                END
            ),
            transaction_count = transaction_count - 
                CASE
                    WHEN OLD.from_account = OLD.to_account THEN 0
                    ELSE 1
                END
        WHERE account = OLD.to_account; 
        
        UPDATE accounts
        SET actual_value = actual_value + (
                CASE
                    WHEN NEW.from_account_type = 'assets'
                        AND NEW.to_account_type IN ('assets','expenses','liabilities','equity')
                        THEN -NEW.amount
                    
                    WHEN NEW.from_account_type = 'liabilities'
                        AND NEW.to_account_type IN ('liabilities','expenses','equity')
                        THEN -NEW.amount

                    WHEN NEW.from_account_type = 'equity'
                        AND NEW.to_account_type IN ('assets','expenses')
                        THEN -NEW.amount
                    
                    ELSE NEW.amount
                END
            ),
            transaction_count = transaction_count + 1
        WHERE account = NEW.from_account;

        UPDATE accounts
        SET actual_value = actual_value + (
                CASE
                    WHEN NEW.to_account_type = 'liabilities'
                        AND NEW.from_account_type = 'assets'
                        THEN -NEW.amount

                    WHEN NEW.to_account_type = 'equity'
                        AND NEW.from_account_type IN ('assets','liabilities')
                        THEN -NEW.amount

                    ELSE NEW.amount
                END
            ),
            transaction_count = transaction_count + 
                CASE
                    WHEN NEW.from_account = NEW.to_account THEN 0
                    ELSE 1
                END
        WHERE account = NEW.to_account;

        UPDATE daily_total
        SET amount = amount - (
            CASE
                WHEN OLD.from_account_type = 'assets'
                    AND OLD.to_account_type IN ('assets','expenses','liabilities','equity')
                    THEN -OLD.amount 

                WHEN OLD.from_account_type = 'liabilities'
                    AND OLD.to_account_type IN ('liabilities','expenses','equity')
                    THEN -OLD.amount

                WHEN OLD.from_account_type = 'equity'
                    AND OLD.to_account_type IN ('assets','expenses')
                    THEN -OLD.amount
                
                ELSE OLD.amount
            END
            ),
            transaction_count = transaction_count - 1
        WHERE day = OLD.day AND month = OLD.month AND year = OLD.year AND account = OLD.from_account AND account_type = OLD.from_account_type;

        UPDATE daily_total
        SET amount = amount - (
            CASE
                WHEN OLD.to_account_type = 'liabilities'
                    AND OLD.from_account_type = 'assets'
                    THEN -OLD.amount

                WHEN OLD.to_account_type = 'equity'
                    AND OLD.from_account_type IN ('assets','liabilities')
                    THEN -OLD.amount

                ELSE OLD.amount
            END
            ),
            transaction_count = transaction_count - 
                CASE
                    WHEN OLD.from_account = OLD.to_account THEN 0
                    ELSE 1
                END
        WHERE day = OLD.day AND month = OLD.month AND year = OLD.year AND account = OLD.to_account AND account_type = OLD.to_account_type;

        UPDATE daily_total
        SET amount = amount + (
            CASE
                WHEN NEW.from_account_type = 'assets'
                    AND NEW.to_account_type IN ('assets','expenses','liabilities','equity')
                    THEN -NEW.amount 

                WHEN NEW.from_account_type = 'liabilities'
                    AND NEW.to_account_type IN ('liabilities','expenses','equity')
                    THEN -NEW.amount

                WHEN NEW.from_account_type = 'equity'
                    AND NEW.to_account_type IN ('assets','expenses')
                    THEN -NEW.amount
                
                ELSE NEW.amount
            END
            ),
            transaction_count = transaction_count + 1
        WHERE day = NEW.day AND month = NEW.month AND year = NEW.year AND account = NEW.from_account AND account_type = NEW.from_account_type;

        UPDATE daily_total
        SET amount = amount + (
            CASE
                WHEN NEW.to_account_type = 'liabilities'
                    AND NEW.from_account_type = 'assets'
                    THEN -NEW.amount

                WHEN NEW.to_account_type = 'equity'
                    AND NEW.from_account_type IN ('assets','liabilities')
                    THEN -NEW.amount

                ELSE NEW.amount
            END
            ),
            transaction_count = transaction_count + 
                CASE
                    WHEN NEW.from_account = NEW.to_account THEN 0
                    ELSE 1
                END
        WHERE day = NEW.day AND month = NEW.month AND year = NEW.year AND account = NEW.to_account AND account_type = NEW.to_account_type;
    END;
    '''
    cursor.execute(insert_trigger)
    cursor.execute(remove_trigger)
    cursor.execute(update_trigger)

    cursor.execute('SELECT account_type FROM account_types')
    if len(cursor.fetchall()) == 0:
        cursor.execute('INSERT INTO account_types (account_type) VALUES ("assets"), ("liabilities"), ("equity"), ("revenue"), ("expenses");')

    cursor.execute('SELECT account FROM accounts')
    if len(cursor.fetchall()) > 0:
        load_page('accounting_page')
    else:
        load_page('signup_initialise_page')

    connect.commit()
    connect.close()

def app_startup():
    load_page('bootoption_page')

def stress_test():
    connect = sql.connect('database.db')
    cursor = connect.cursor()
    cursor.execute('PRAGMA foreign_keys = ON')
    dates = date(2022,8,1)
    for i in range(100000):
        ints = random.randint(10,100)
        current_date = dates + timedelta(days=i)
        date_str = current_date.strftime("%d-%m-%Y")
        date_list = date_str.split('-')
        cursor.execute('INSERT INTO transactions (from_account_type, from_account, to_account_type, to_account, day, month, year, description, amount) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',['assets','cash','expenses','groceries',date_list[0],date_list[1],date_list[2],'STRESS TEST',ints])

    connect.commit()
    connect.close()

def combobox_date(cmb1,cmb2,cmb3,select= str in ['month','year']):
    year = cmb3.get()
    month = cmb2.get()

    if select == 'year':
        cmb2.set('')
        cmb1.set('')
        cmb1.configure(values=[])
        if year != '':
            cmb2.configure(values=['']+[1,2,3,4,5,6,7,8,9,10,11,12])
        else:
            cmb2.configure(values=[])
    
    elif select == 'month':
        cmb1.set('')
        if year != '' and month != '':
            year = int(year)
            month = int(month)

            if month == 12:
                next_month = date(year + 1, 1, 1)
            else:
                next_month = date(year, month + 1, 1)
            days_in_month = (next_month - timedelta(days=1)).day

            cmb1.configure(values=[''] + list(range(1, days_in_month + 1)))
        else:
            cmb1.configure(values=[])
def combobox_date_set_year(cmb):
    cmb.set('')
    current_year = date.today().year
    cmb.configure(values=[''] + [i for i in range(2000,current_year+1)])

#stress_test()
app_startup()
print(f"Startup time:{perf_counter() - start:.3f}seconds")
window.mainloop()
#load_page('accounting_page')