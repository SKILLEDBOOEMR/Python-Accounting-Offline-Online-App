from tkinter import Label,LabelFrame,Entry,Frame,Button,Canvas,BooleanVar,END,Tk,Widget
from tkinter import ttk as ttk
from PIL import Image, ImageTk
import requests
from dotenv import load_dotenv
from os import getenv,path
from threading import Thread
from time import time
import json
from ctypes import windll
from datetime import datetime, date
import sqlite3 as sql
start_time = time()

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


window = Tk()
window.title('Budgit')
window.geometry('1400x800')
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

style.configure('Treeview',background = light_dark, foreground=main_color,font=('monogram',20,'bold'), fieldbackground=light_dark,borderwidth=0)
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

    def offline_add_entry(self,from_type_widget,from_account_widget,to_type_widget,to_account_widget,error_msg_widget,date_widget,amount_widget,description_widget):
        from_type = from_type_widget.get()
        from_account = from_account_widget.get()
        to_type = to_type_widget.get()
        to_account = to_account_widget.get()
        date= date_widget.get()
        amount = amount_widget.get()
        description = description_widget.get()

        if not all([from_type, from_account, to_type, to_account, date, amount, description]):
            error_msg_widget.configure(text='Please fill in all fields')
            return False, []

        try:
            amount = int(amount)
        except Exception:
            error_msg_widget.configure(text='Make sure amount is an integer')
            return False, []
        
        if amount < 0:
            error_msg_widget.configure(text='Please input a positive value in amount')
            return False, []
        
        try:
            date = datetime.strptime(date,'%d-%m-%Y')
            date = datetime.strftime(date,'%d-%m-%Y')
        except Exception as e:
            error_msg_widget.configure(text='Invalid Date make sure its DD-MM-YY format and be in calendar')
            return False, []


        date_list = date.split('-')

        connect = sql.connect('database.db')
        cursor = connect.cursor()

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
        date= date_widget.get()
        amount = amount_widget.get()
        description = description_widget.get()

        try:
            amount = int(amount)
        except Exception:
            error_msg_widget.configure(text='Invalid number inputted in ammount entry')
            return False,[]

        try:
            date = datetime.strptime(date,'%d-%m-%Y')
            date = datetime.strftime(date,'%d-%m-%Y')
        except Exception as e:
            error_msg_widget.configure(text='Invalid Date make sure its DD-MM-YY format and be in calendar')
            return False,[]

        connect = sql.connect('database.db')
        cursor = connect.cursor()

        split_date = date.split('-')
        #Update the new transaction
        cursor.execute('UPDATE transactions SET from_account_type = ?, from_account = ?, to_account_type = ?, to_account = ?, day = ?, month = ?, year = ?, description = ?, amount = ? WHERE id = ?', (from_type,from_account,to_type,to_account,split_date[0],split_date[1],split_date[2],description,amount,ids))

        error_msg_widget.configure(fg=success_color,text='Sucessfully edited a log in Transactions')
        window.after(3000,lambda:error_msg_widget.configure(fg=error_color,text=''))

        connect.commit()
        connect.close()

        if search_return_list == True:
            return True,[from_type,from_account,to_type,to_account,date,description,amount]
        else:
            return True,[]

    def offline_set_treeview_with_params(self,treeview,param_dict,search_return_list=False):
        def function(widget_data,type_transform,column_name,query,params):
            if widget_data != '':
                try:
                    updated_value = type_transform(widget_data)
                    if column_name == 'description':
                        query += f'AND {column_name} LIKE ?'
                        params.append(f'%{updated_value}%')
                    else:
                        query += f" AND {column_name} = ?"
                        params.append(updated_value)
                except Exception as e:
                    print(e)
            return query 

        for children in treeview.get_children():
            treeview.delete(children)

        query = 'SELECT * FROM transactions WHERE 1=1'
        params = []

        connect = sql.connect('database.db')
        cursor = connect.cursor()

        try:
            for i in param_dict:
                widget_name = param_dict[i]['widget_data']
                type_convert = param_dict[i]['type']
                column_name = i
                query = function(widget_name,type_convert,column_name,query,params)

        except Exception as e:
            print(e)
            return False

        cursor.execute(query, params)
        results = cursor.fetchall()
        connect.commit()
        connect.close()

        if search_return_list:
            return results
        else:
            for index,i in enumerate(results):
                date = '-'.join([str(i[5]),str(i[6]),str(i[7])])
                treeview.insert('','end',values=[index+1,i[0],i[1],i[2],i[3],i[4],date,i[8],i[9]])
    
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
        cursor.execute('SELECT account_type,account,transaction_count,actual_value FROM accounts ')
        temp = cursor.fetchall()
        connect.close()
        return temp

    def offline_add_account(self,type_widget,account_widget,error_msg_widget):
        types = type_widget.get()
        account = account_widget.get()
        print(types,account)

        if types == '' or account in ['\u200BEnter Here','']:
            error_msg_widget.configure(fg=error_color,text='Please fill in all the Entry Fields')
            window.after(3000,lambda:error_msg_widget.configure(fg=error_color,text=''))
            return False,[]
        
        connect = sql.connect('database.db')
        cursor = connect.cursor()
        try:
            cursor.execute('INSERT INTO accounts (account,account_type) VALUES (?,?)', [account,types])
        except Exception as e:
            connect.close()
            error_msg_widget.configure(fg=error_color,text='Account Already Exists!')
            window.after(3000,lambda:error_msg_widget.configure(fg=error_color,text=''))
            return False, []
        
        connect.commit()
        connect.close()
        
        error_msg_widget.configure(fg=success_color,text='Succesfully Added a New Account')
        window.after(3000,lambda:error_msg_widget.configure(fg=error_color,text=''))
        return True, [types,account,0,0]
        

class GUI:
    def __init__(self):
        #Transaction page add part
        self.accountingpage_transactionpage_addpage_status = False
        self.accountingpage_transactionpage_removepage_status = False
        self.accountingpage_transactionpage_editpage_status = False

        self.selection_status_confirm = False

        #main config stuff
        self.account_list = []
        self.category_list =[]

        self.account_type = ['assets','liabilities','equity','revenue','expenses']

        #Check whether user use online or offline mode
        self.is_online = False


        #The ID value for Selection in trasanction page
        self.treeview_id = int
        self.treeview_selected_row = None
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
                print(targeted_account)
                print(lists[i][types])
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
            for item in category_treeview.get_children():
                category_treeview.delete(item)

            if getattr(state,'is_online') == False :
                lists = api.offline_fetch_accounts()
                for index,row in enumerate(lists):
                    category_treeview.insert('','end',values=[*[index+1],*row])
                category_data_label1.configure(text=len(lists))
            
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
    build_accounting_page_transaction(accountingpage_subframe2_frame2)

    #Category page
    accountingpage_subframe2_frame3 = Frame(accountingpage_mainframe2,background='white')
    category_treeview,category_data_label1 = build_accounting_page_category(accountingpage_subframe2_frame3)


    accountingpage_subframe2_frame4 = Frame(accountingpage_mainframe2,background=sub_maincolor)

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
def build_accounting_page_transaction(master):
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
            for children in accountingpage_subframe2_frame2_treeview.get_children():
                accountingpage_subframe2_frame2_treeview.delete(children)

            if accountingpage_subframe2_frame2_infopage_frame1_combobox1.get() != '': day = int(accountingpage_subframe2_frame2_infopage_frame1_combobox1.get()) 
            else: day = accountingpage_subframe2_frame2_infopage_frame1_combobox1.get()
            if accountingpage_subframe2_frame2_infopage_frame1_combobox2.get() != '': month = int(accountingpage_subframe2_frame2_infopage_frame1_combobox2.get())
            else: month = accountingpage_subframe2_frame2_infopage_frame1_combobox2.get()
            if accountingpage_subframe2_frame2_infopage_frame1_combobox3.get() != '': year = int(accountingpage_subframe2_frame2_infopage_frame1_combobox3.get())
            else: year = accountingpage_subframe2_frame2_infopage_frame1_combobox3.get()

            connect = sql.connect('database.db')
            cursor = connect.cursor()

            if day != '' or month != '' or year != '':
                query = 'SELECT * FROM transactions WHERE 1=1'
                params = []

                if day != '':
                    query += ' AND day = ?'
                    params.append(day)

                if month != '' :
                    query += ' AND month = ?'
                    params.append(month)

                if year != '':
                    query += ' AND year = ?'
                    params.append(year)

                cursor.execute(query, params)
                results = cursor.fetchall()

                for index,i in enumerate(results):
                    date = '-'.join([str(i[5]),str(i[6]),str(i[7])])
                    accountingpage_subframe2_frame2_treeview.insert('','end',values=[index+1,i[0],i[1],i[2],i[3],i[4],date,i[8],i[9]])
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
        accountingpage_subframe2_frame2_buttonpage_labelframe3_entry1.configure(state='normal')
        accountingpage_subframe2_frame2_buttonpage_labelframe3_entry2.configure(state='normal')
        accountingpage_subframe2_frame2_buttonpage_labelframe3_entry3.configure(state='normal')

        accountingpage_subframe2_frame2_buttonpage_labelframe1_entry1.set('')
        accountingpage_subframe2_frame2_buttonpage_labelframe1_entry2.set('')
        accountingpage_subframe2_frame2_buttonpage_labelframe2_entry1.set('')
        accountingpage_subframe2_frame2_buttonpage_labelframe2_entry2.set('')
        accountingpage_subframe2_frame2_buttonpage_labelframe3_entry2.delete(0,END)
        accountingpage_subframe2_frame2_buttonpage_labelframe3_entry2.insert(0,'\u200BEnter here')
        accountingpage_subframe2_frame2_buttonpage_labelframe3_entry2.configure(fg=sub_textcolor)
        accountingpage_subframe2_frame2_buttonpage_labelframe3_entry3.delete(0,END)
        accountingpage_subframe2_frame2_buttonpage_labelframe3_entry3.configure(fg=sub_textcolor)
        accountingpage_subframe2_frame2_buttonpage_labelframe3_entry3.insert(0,'\u200Beg.1000')
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
                accountingpage_subframe2_frame2_buttonpage_labelframe3_entry1.configure(state='normal',fg=text_color)
                accountingpage_subframe2_frame2_buttonpage_labelframe3_entry2.configure(state='normal',fg=text_color)
                accountingpage_subframe2_frame2_buttonpage_labelframe3_entry3.configure(state='normal',fg=text_color)
                accountingpage_subframe2_frame2_infopage_frame2.grid_forget()
                accountingpage_subframe2_frame2_infopage_dataframe.grid_forget()
                accountingpage_subframe2_frame2_buttonpage.grid(column=0,row=0,sticky='nsew')

                treeview_values = accountingpage_subframe2_frame2_treeview.item(value,'values')
                accountingpage_subframe2_frame2_buttonpage_labelframe1_entry1.set(treeview_values[2])
                accountingpage_subframe2_frame2_buttonpage_labelframe1_entry2.set(treeview_values[3])
                accountingpage_subframe2_frame2_buttonpage_labelframe2_entry1.set(treeview_values[4])
                accountingpage_subframe2_frame2_buttonpage_labelframe2_entry2.set(treeview_values[5])
                accountingpage_subframe2_frame2_buttonpage_labelframe3_entry1.delete(0,END)
                accountingpage_subframe2_frame2_buttonpage_labelframe3_entry1.insert(0,treeview_values[6])
                accountingpage_subframe2_frame2_buttonpage_labelframe3_entry2.delete(0,END)
                accountingpage_subframe2_frame2_buttonpage_labelframe3_entry2.insert(0,treeview_values[7])
                accountingpage_subframe2_frame2_buttonpage_labelframe3_entry3.delete(0,END)
                accountingpage_subframe2_frame2_buttonpage_labelframe3_entry3.insert(0,treeview_values[8])
                state.treeview_id = treeview_values[1]


                set_custom_combobox_value(accountingpage_subframe2_frame2_buttonpage_labelframe1_entry2,accountingpage_subframe2_frame2_messages_label1,accountingpage_subframe2_frame2_buttonpage_labelframe1_entry1,True)
                set_combobox_account_type(accountingpage_subframe2_frame2_buttonpage_labelframe2_entry1,accountingpage_subframe2_frame2_messages_label1,accountingpage_subframe2_frame2_buttonpage_labelframe1_entry1,True)
                set_custom_combobox_value(accountingpage_subframe2_frame2_buttonpage_labelframe2_entry2,accountingpage_subframe2_frame2_messages_label1,accountingpage_subframe2_frame2_buttonpage_labelframe2_entry1,True)

                if lock:
                    accountingpage_subframe2_frame2_buttonpage_labelframe1_entry1.configure(state='disabled')
                    accountingpage_subframe2_frame2_buttonpage_labelframe1_entry2.configure(state='disabled')
                    accountingpage_subframe2_frame2_buttonpage_labelframe2_entry1.configure(state='disabled')
                    accountingpage_subframe2_frame2_buttonpage_labelframe2_entry2.configure(state='disabled')
                    accountingpage_subframe2_frame2_buttonpage_labelframe3_entry1.configure(state='disabled')
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
                is_success, data = api.offline_add_entry(accountingpage_subframe2_frame2_buttonpage_labelframe1_entry1,accountingpage_subframe2_frame2_buttonpage_labelframe1_entry2,accountingpage_subframe2_frame2_buttonpage_labelframe2_entry1,accountingpage_subframe2_frame2_buttonpage_labelframe2_entry2,accountingpage_subframe2_frame2_messages_label1,accountingpage_subframe2_frame2_buttonpage_labelframe3_entry1,accountingpage_subframe2_frame2_buttonpage_labelframe3_entry3,accountingpage_subframe2_frame2_buttonpage_labelframe3_entry2)
                if is_success:
                    number = len(accountingpage_subframe2_frame2_treeview.get_children()) + 1
                    accountingpage_subframe2_frame2_treeview.insert('','end',values=[*[number],*data])
                    reset()
                    to_button_page('add')

            if type_of_command == 'remove':
                is_success = api.offline_remove_entry(error_msg_widget=accountingpage_subframe2_frame2_messages_label1,ids=int(state.treeview_id))
                if is_success:
                    to_button_page('remove')
                    new_list = []
                    for item in accountingpage_subframe2_frame2_treeview.get_children():
                        if item != state.treeview_selected_row:
                            new_list.append(accountingpage_subframe2_frame2_treeview.item(item,'values'))
                        accountingpage_subframe2_frame2_treeview.delete(item)
                    
                    for i,value in enumerate(new_list):
                        edited_list = value[1:]
                        accountingpage_subframe2_frame2_treeview.insert('','end',values=[*[i],*edited_list])

            if type_of_command == 'edit':
                is_success, data = api.offline_edit_entry(state.treeview_id,accountingpage_subframe2_frame2_buttonpage_labelframe1_entry1,accountingpage_subframe2_frame2_buttonpage_labelframe1_entry2,accountingpage_subframe2_frame2_buttonpage_labelframe2_entry1,accountingpage_subframe2_frame2_buttonpage_labelframe2_entry2,accountingpage_subframe2_frame2_messages_label1,accountingpage_subframe2_frame2_buttonpage_labelframe3_entry1,accountingpage_subframe2_frame2_buttonpage_labelframe3_entry3,accountingpage_subframe2_frame2_buttonpage_labelframe3_entry2,search_return_list=True)
                if is_success:
                    to_button_page('edit')
                    value = accountingpage_subframe2_frame2_treeview.item(state.treeview_selected_row,'values')
                    accountingpage_subframe2_frame2_treeview.item(state.treeview_selected_row,values=[*value[:2], *data])

            if type_of_command == 'search':
                from_type = accountingpage_subframe2_frame2_buttonpage_labelframe1_entry1.get()
                from_account = accountingpage_subframe2_frame2_buttonpage_labelframe1_entry2.get()
                to_type = accountingpage_subframe2_frame2_buttonpage_labelframe2_entry1.get()
                to_account = accountingpage_subframe2_frame2_buttonpage_labelframe2_entry2.get()
                date = accountingpage_subframe2_frame2_buttonpage_labelframe3_entry1.get()
                description  = accountingpage_subframe2_frame2_buttonpage_labelframe3_entry2.get()
                amount = accountingpage_subframe2_frame2_buttonpage_labelframe3_entry3.get()

                param_dict = {}

                if from_type != '':
                    param_dict.update({
                        'from_account_type': {
                            'widget_data' : from_type,
                            'type' : str
                        }
                    })

                if from_account != '':
                    param_dict.update({
                        'from_account': {
                            'widget_data' : from_account,
                            'type' : str
                        }
                    })

                if to_type != '':
                    param_dict.update({
                        'to_account_type': {
                            'widget_data' : to_type,
                            'type' : str
                        }
                    })

                if to_account != '':
                    param_dict.update({
                        'to_account': {
                            'widget_data' : to_account,
                            'type' : str
                        }
                    })

                if date != '\u200bDD-MM-YY' and date != '':
                    date_list = date.split('-')
                    if 0 < len(date_list) < 3 :
                        accountingpage_subframe2_frame2_messages_label1.configure(text='The date is in the wrong format')
                        return False

                    if date_list[0] != '00' and date_list[0] != '0':
                        try:
                            day = int(date_list[0])
                            if day < 0 or day > 31:
                                accountingpage_subframe2_frame2_messages_label1.configure(text='Invalid Day Number')
                                return False
                        except Exception:
                            accountingpage_subframe2_frame2_messages_label1.configure(text='Invalid Day Number')
                            return False
                        
                        param_dict.update({
                            'day' : {
                                'widget_data' : day,
                                'type' : int
                            }

                        })

                    if date_list[1] != '00' and date_list[1] != '0':
                        try:
                            month = int(date_list[1])
                            if month < 0 or month > 12:
                                accountingpage_subframe2_frame2_messages_label1.configure(text='Invalid Month Number')
                                return False
                        except Exception:
                            accountingpage_subframe2_frame2_messages_label1.configure(text='Invalid Month Number')
                            return False
                        
                        param_dict.update({
                            'month' : {
                                'widget_data' : month,
                                'type' : int
                            }

                        })

                    if date_list[2] != '0000':
                        try:
                            datetime.strptime(date_list[2],'%Y')
                        except Exception:
                            accountingpage_subframe2_frame2_messages_label1.configure(text='Invalid Year Number')
                            return False
                        
                        param_dict.update({
                            'year' : {
                                'widget_data' : date_list[2],
                                'type' : int
                            }

                        })


                if description != '\u200BEnter here' and description != '':
                    param_dict.update({
                        'description': {
                            'widget_data' : description,
                            'type' : str
                        }
                    })

                if amount != '\u200beg.1000' and amount != '':
                    param_dict.update({
                        'amount': {
                            'widget_data' : amount,
                            'type' : int
                        }
                    })

                api.offline_set_treeview_with_params(accountingpage_subframe2_frame2_treeview,param_dict=param_dict)
                accountingpage_subframe2_frame2_messages_label1.configure(fg=success_color,text='Sucessfully searched in Transactions')
                window.after(3000,lambda:accountingpage_subframe2_frame2_messages_label1.configure(fg=error_color,text=''))

    def calendar_search_function(event):
        date_search_dict_param = {
            'day':{
                'widget_data' : accountingpage_subframe2_frame2_infopage_frame1_combobox1.get(),
                'type' : int
            },
            'month' : {
                'widget_data' : accountingpage_subframe2_frame2_infopage_frame1_combobox2.get(),
                'type' : int
            },
            'year' : {
                'widget_data' : accountingpage_subframe2_frame2_infopage_frame1_combobox3.get(),
                'type' : int
            },
        }

        api.offline_set_treeview_with_params(accountingpage_subframe2_frame2_treeview,date_search_dict_param)

    accountingpage_subframe2_frame2_transactionpage = Frame(master, background=sub_lightdark)
    accountingpage_subframe2_frame2_transactionpage.grid(column=0,row=0,sticky='nsew')

    accountingpage_subframe2_frame2_scrollbar = ttk.Scrollbar(accountingpage_subframe2_frame2_transactionpage)
    accountingpage_subframe2_frame2_scrollbar.pack(side='right',fill='y',pady=(0,5))

    headings = ('No.','ID','From','From2','To','To2','Date','Description','Amount')
    accountingpage_subframe2_frame2_treeview = ttk.Treeview(accountingpage_subframe2_frame2_transactionpage,columns=headings, show='headings',yscrollcommand=accountingpage_subframe2_frame2_scrollbar,selectmode='browse')
    accountingpage_subframe2_frame2_scrollbar.configure(command=accountingpage_subframe2_frame2_treeview.yview)

    accountingpage_subframe2_frame2_treeview.column('No.',anchor='w',stretch=True,minwidth=30,width=30)
    accountingpage_subframe2_frame2_treeview.heading('No.', text = 'No.')

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
    accountingpage_subframe2_frame2_infopage_dataframe.grid_columnconfigure((0,5),weight=1)
    accountingpage_subframe2_frame2_infopage_dataframe.grid_rowconfigure((0,1,2,3),weight=1)

    accountingpage_subframe2_frame2_infopage_label1 = Label(accountingpage_subframe2_frame2_infopage_dataframe, text='Date', background=sub_lightdark, fg=text_color,font=('monogram',20))
    accountingpage_subframe2_frame2_infopage_label1.grid(column=0,row=0,sticky='nsw',pady=5,padx=[3,0])
    accountingpage_subframe2_frame2_infopage_equal1 = Label(accountingpage_subframe2_frame2_infopage_dataframe, text=':', background=sub_lightdark, fg=text_color,font=('monogram',20))
    accountingpage_subframe2_frame2_infopage_equal1.grid(column=1,row=0,sticky='nsew',pady=5)
    accountingpage_subframe2_frame2_infopage_frame1 = Frame(accountingpage_subframe2_frame2_infopage_dataframe,background=sub_lightdark)
    accountingpage_subframe2_frame2_infopage_frame1_combobox1 = ttk.Combobox(accountingpage_subframe2_frame2_infopage_frame1, background = light_dark, foreground = text_color,font=('monogram',20),state='readonly',width=5,values=[''] + list(range(1,32)))
    accountingpage_subframe2_frame2_infopage_frame1_combobox1.grid(column=0,row=0,sticky='ew')
    accountingpage_subframe2_frame2_infopage_frame1_combobox2 = ttk.Combobox(accountingpage_subframe2_frame2_infopage_frame1, background = light_dark, foreground = text_color,font=('monogram',20),state='readonly',width=10,values =[''] +  list(range(1,13)))
    accountingpage_subframe2_frame2_infopage_frame1_combobox2.grid(column=1,row=0,sticky='ew',padx=5)
    accountingpage_subframe2_frame2_infopage_frame1_combobox3 = ttk.Combobox(accountingpage_subframe2_frame2_infopage_frame1, background = light_dark, foreground = text_color,font=('monogram',20),state='readonly',width=5, values= [''] + [str(y) for y in range(2000, date.today().year + 1)])
    accountingpage_subframe2_frame2_infopage_frame1_combobox3.grid(column=2,row=0,sticky='ew')

    #Set the current date as default
    current_date = datetime.today().strftime('%d/%m/%Y').split('/')
    accountingpage_subframe2_frame2_infopage_frame1_combobox1.set(current_date[0])
    accountingpage_subframe2_frame2_infopage_frame1_combobox2.set(current_date[1])
    accountingpage_subframe2_frame2_infopage_frame1_combobox3.set(current_date[2])
    
    accountingpage_subframe2_frame2_infopage_frame1_combobox1.bind('<<ComboboxSelected>>', calendar_search_function)
    accountingpage_subframe2_frame2_infopage_frame1_combobox2.bind('<<ComboboxSelected>>', calendar_search_function)
    accountingpage_subframe2_frame2_infopage_frame1_combobox3.bind('<<ComboboxSelected>>', calendar_search_function)

    accountingpage_subframe2_frame2_infopage_frame1.grid_columnconfigure([0,2], weight=1)
    accountingpage_subframe2_frame2_infopage_frame1.grid_columnconfigure(1, weight=2)
    accountingpage_subframe2_frame2_infopage_frame1.grid_rowconfigure(0,weight=1)
    accountingpage_subframe2_frame2_infopage_frame1.grid(column=2,row=0,sticky='nsew',pady=5, padx=[0,5])

    accountingpage_subframe2_frame2_infopage_label2 = Label(accountingpage_subframe2_frame2_infopage_dataframe, text='Total Income', background=sub_lightdark, fg=text_color,font=('monogram',20))
    accountingpage_subframe2_frame2_infopage_label2.grid(column=0,row=1,sticky='nsw',pady=(0,5),padx=[3,0])
    accountingpage_subframe2_frame2_infopage_equal2 = Label(accountingpage_subframe2_frame2_infopage_dataframe, text=':', background=sub_lightdark, fg=text_color,font=('monogram',20))
    accountingpage_subframe2_frame2_infopage_equal2.grid(column=1,row=1,sticky='nsew',pady=5)
    accountingpage_subframe2_frame2_infopage_label3 = Label(accountingpage_subframe2_frame2_infopage_dataframe, text='0', background=sub_lightdark, fg='#2ECC71',font=('monogram',20))
    accountingpage_subframe2_frame2_infopage_label3.grid(column=2,row=1,sticky='nsw',pady=(0,5))    
    
    accountingpage_subframe2_frame2_infopage_label4 = Label(accountingpage_subframe2_frame2_infopage_dataframe, text='Total Expenses', background=sub_lightdark, fg=text_color,font=('monogram',20))
    accountingpage_subframe2_frame2_infopage_label4.grid(column=0,row=2,sticky='nsw',pady=(0,5),padx=[3,0])
    accountingpage_subframe2_frame2_infopage_equal3 = Label(accountingpage_subframe2_frame2_infopage_dataframe, text=':', background=sub_lightdark, fg=text_color,font=('monogram',20))
    accountingpage_subframe2_frame2_infopage_equal3.grid(column=1,row=2,sticky='nsew',pady=5)
    accountingpage_subframe2_frame2_infopage_label5 = Label(accountingpage_subframe2_frame2_infopage_dataframe, text='0', background=sub_lightdark, fg='#E57373',font=('monogram',20))
    accountingpage_subframe2_frame2_infopage_label5.grid(column=2,row=2,sticky='nsw',pady=(0,5))    

    accountingpage_subframe2_frame2_infopage_label6 = Label(accountingpage_subframe2_frame2_infopage_dataframe, text='Net Balance', background=sub_lightdark, fg=text_color,font=('monogram',20))
    accountingpage_subframe2_frame2_infopage_label6.grid(column=0,row=3,sticky='nsw',pady=(0,5),padx=[3,0])
    accountingpage_subframe2_frame2_infopage_equal4 = Label(accountingpage_subframe2_frame2_infopage_dataframe, text=':', background=sub_lightdark, fg=text_color,font=('monogram',20))
    accountingpage_subframe2_frame2_infopage_equal4.grid(column=1,row=3,sticky='nsew',pady=5)
    accountingpage_subframe2_frame2_infopage_label7 = Label(accountingpage_subframe2_frame2_infopage_dataframe, text='0', background=sub_lightdark, fg=text_color,font=('monogram',20))
    accountingpage_subframe2_frame2_infopage_label7.grid(column=2,row=3,sticky='nsw',pady=(0,5))    

    accountingpage_subframe2_frame2_infopage_label8 = Label(accountingpage_subframe2_frame2_infopage_dataframe, text='Current Balance', background=sub_lightdark, fg=text_color,font=('monogram',20))
    accountingpage_subframe2_frame2_infopage_label8.grid(column=3,row=0,sticky='nsw',pady=(0,5),padx=(3,0))
    accountingpage_subframe2_frame2_infopage_equal5 = Label(accountingpage_subframe2_frame2_infopage_dataframe, text=':', background=sub_lightdark, fg=text_color,font=('monogram',20))
    accountingpage_subframe2_frame2_infopage_equal5.grid(column=4,row=0,sticky='nsew',pady=5)
    accountingpage_subframe2_frame2_infopage_label9 = Label(accountingpage_subframe2_frame2_infopage_dataframe, text='0', background=sub_lightdark, fg=text_color,font=('monogram',20))
    accountingpage_subframe2_frame2_infopage_label9.grid(column=5,row=0,sticky='nsw',pady=(0,5))   

    accountingpage_subframe2_frame2_infopage_label10 = Label(accountingpage_subframe2_frame2_infopage_dataframe, text='Total Transactions', background=sub_lightdark, fg=text_color,font=('monogram',20))
    accountingpage_subframe2_frame2_infopage_label10.grid(column=3,row=1,sticky='nsw',pady=(0,5),padx=(3,0))
    accountingpage_subframe2_frame2_infopage_equal6 = Label(accountingpage_subframe2_frame2_infopage_dataframe, text=':', background=sub_lightdark, fg=text_color,font=('monogram',20))
    accountingpage_subframe2_frame2_infopage_equal6.grid(column=4,row=1,sticky='nsew',pady=5)
    accountingpage_subframe2_frame2_infopage_label11 = Label(accountingpage_subframe2_frame2_infopage_dataframe, text='0', background=sub_lightdark, fg=text_color,font=('monogram',20))
    accountingpage_subframe2_frame2_infopage_label11.grid(column=5,row=1,sticky='nsw',pady=(0,5))   

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
    accountingpage_subframe2_frame2_buttonpage
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
    accountingpage_subframe2_frame2_buttonpage_labelframe3_entry1 = Entry(accountingpage_subframe2_frame2_buttonpage_labelframe3, background = light_dark, fg = text_color,font=('monogram',20),disabledbackground=light_dark,disabledforeground=text_color)
    accountingpage_subframe2_frame2_buttonpage_labelframe3_entry1.insert(0,datetime.today().strftime('%d-%m-%Y'))
    accountingpage_subframe2_frame2_buttonpage_labelframe3_entry1.bind('<FocusIn>', lambda event: entry_text(accountingpage_subframe2_frame2_buttonpage_labelframe3_entry1,['\u200BDD-MM-YY']))
    accountingpage_subframe2_frame2_buttonpage_labelframe3_entry1.bind('<FocusOut>', lambda event: entry_text(accountingpage_subframe2_frame2_buttonpage_labelframe3_entry1,['\u200BDD-MM-YY'],True,'\u200BDD-MM-YY'))
    accountingpage_subframe2_frame2_buttonpage_labelframe3_entry1.grid(column=2,row=0,sticky='new',pady=5,padx=[0,5])

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

    if getattr(state, 'is_online') == False:
        print('hello')



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

    #Command to place the uhh transaction list according to the uhh date :)
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
        def treeview_select(event=None,lock=bool):
            accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame1.pack_forget()
            accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame2.pack_forget()
            accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3.pack(side='top',fill='both',expand=1)
            focused = accountingpage_subframe2_frame3_categorypage_leftframe_frame1_treeview.focus()
            value = accountingpage_subframe2_frame3_categorypage_leftframe_frame1_treeview.item(focused,'values')

            if not value or len(value) < 5:
                return

            accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3_labelframe1_combobox1.set(value[1])
            accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3_labelframe1_entry1.delete(0,END)
            accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3_labelframe1_entry1.insert(0,value[2])
            accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3_labelframe1_entry1.configure(fg=text_color)
            accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3_labelframe2_label2.configure(text=value[3])
            accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3_labelframe2_label4.configure(text=value[4])

            if lock:
                accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3_labelframe1_combobox1.configure(state='disabled')
                accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3_labelframe1_entry1.configure(state='disabled')

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
                accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame2.pack(side='top',fill='both',expand=1)
                accountingpage_subframe2_frame3_categorypage_leftframe_frame1_treeview.bind('<<TreeviewSelect>>',lambda event :treeview_select(event=event,lock=True))

                accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3_labelframe1_combobox1.configure(state='disabled')
                accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3_labelframe1_entry1.configure(state='disabled')
                accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3_frame1_button2.configure(text='Remove')

            if type_of_command == 'edit':
                reset_button_page()
                accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3.pack_forget()
                accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame2.pack(side='top',fill='both',expand=1)
                accountingpage_subframe2_frame3_categorypage_leftframe_frame1_treeview.bind('<<TreeviewSelect>>',lambda event :treeview_select(event=event,lock=False))

                accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3_labelframe1_combobox1.configure(state='readonly')
                accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3_labelframe1_entry1.configure(state='normal')
                accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3_frame1_button2.configure(text='Edit')

                accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3_labelframe1_combobox1.configure(values=state.account_type)

            if type_of_command == 'search':
                reset_button_page()
                accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame2.pack_forget()
                accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3.pack(side='top',fill='both',expand=1)

                accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3_labelframe1_combobox1.configure(state='readonly')
                accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3_labelframe1_entry1.configure(state='normal')
                accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3_frame1_button2.configure(text='Search')

                account_type =  [''] + state.account_type 
                accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3_labelframe1_combobox1.configure(values=account_type)
    def button_command(type_of_command = str in ['add','remove','edit','search']):
        if getattr(state,'is_online') == False:
            if type_of_command == 'add':
                status, data = api.offline_add_account(accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3_labelframe1_combobox1,accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3_labelframe1_entry1,accountingpage_subframe2_frame3_categorypage_leftframe_frame2_label1)
                if status:
                    accountingpage_subframe2_frame3_categorypage_leftframe_frame1_treeview.insert('','end',values=([len(accountingpage_subframe2_frame3_categorypage_leftframe_frame1_treeview.get_children())+1] + data))
                    to_button_page('add')

            if type_of_command == 'remove':
                print('hello world')

            if type_of_command == 'edit':
                print('hello world')

            if type_of_command == 'search':
                print('hello world')
    def back_button():
        for frame in [accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame2,accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame3]:
            frame.pack_forget()
        accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame1.pack(side='top',fill='both',expand=1)


    master.grid_columnconfigure(0,weight=1)
    master.grid_rowconfigure(0,weight=1)
    accountingpage_subframe2_frame3_categorypage = Frame(master, background=sub_lightdark)
    accountingpage_subframe2_frame3_categorypage.grid(column=0,row=0,sticky='nsew')
    accountingpage_subframe2_frame3_categorypage.grid_columnconfigure(0,weight=4,uniform='a')
    accountingpage_subframe2_frame3_categorypage.grid_columnconfigure(1,weight=3,uniform='a')
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

    headings = ('No.','Type','Account','Entry Count','Balance')
    
    accountingpage_subframe2_frame3_categorypage_leftframe_frame1_treeview = ttk.Treeview(accountingpage_subframe2_frame3_categorypage_leftframe_frame1,columns=headings, show='headings',yscrollcommand=accountingpage_subframe2_frame3_categorypage_leftframe_frame1_scrollbar)
    accountingpage_subframe2_frame3_categorypage_leftframe_frame1_treeview.grid(column=0,row=0,sticky='nsew')
    accountingpage_subframe2_frame3_categorypage_leftframe_frame1_scrollbar.configure(command=accountingpage_subframe2_frame3_categorypage_leftframe_frame1_treeview.yview)

    accountingpage_subframe2_frame3_categorypage_leftframe_frame1_treeview.column('No.',anchor='w',stretch=True,minwidth=35,width=35)
    accountingpage_subframe2_frame3_categorypage_leftframe_frame1_treeview.heading('No.', text = 'No.')

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

    accountingpage_subframe2_frame3_categorypage_leftframe_frame2_label1 = Label(accountingpage_subframe2_frame3_categorypage_leftframe_frame2, text='', background=sub_lightdark, fg=error_color,font=('monogram',20))
    accountingpage_subframe2_frame3_categorypage_leftframe_frame2_label1.pack(side='top',fill='both', expand=True,pady=(3,0),padx=3,anchor='w')

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

    accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame1_labelframe1_label1 = Label(accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame1_labelframe1, text='Accounts in Table', background=sub_lightdark, fg=text_color,font=('monogram',20))
    accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame1_labelframe1_label1.grid(column=0,row=0,sticky='nw',pady=5,padx=[3,0])
    accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame1_labelframe1_equal1 = Label(accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame1_labelframe1, text=':', background=sub_lightdark, fg=text_color,font=('monogram',20))
    accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame1_labelframe1_equal1.grid(column=1,row=0,sticky='nw',pady=5)
    accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame1_labelframe1_label2 = Label(accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame1_labelframe1, text='Bing Bong', background=sub_lightdark, fg=text_color,font=('monogram',20))
    accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame1_labelframe1_label2.grid(column=2,row=0,sticky='nw',pady=5)

    accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame1_labelframe1_label3 = Label(accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame1_labelframe1, text='Highest Transaction Log', background=sub_lightdark, fg=text_color,font=('monogram',20))
    accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame1_labelframe1_label3.grid(column=0,row=1,sticky='nw',pady=5,padx=[3,0])
    accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame1_labelframe1_equal2 = Label(accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame1_labelframe1, text=':', background=sub_lightdark, fg=text_color,font=('monogram',20))
    accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame1_labelframe1_equal2.grid(column=1,row=1,sticky='nw',pady=5)
    accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame1_labelframe1_label4 = Label(accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame1_labelframe1, text='Bing Bong', background=sub_lightdark, fg=text_color,font=('monogram',20))
    accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame1_labelframe1_label4.grid(column=2,row=1,sticky='nw',pady=5)

    accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame1_labelframe1_label5 = Label(accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame1_labelframe1, text='Lowest Transaction Log', background=sub_lightdark, fg=text_color,font=('monogram',20))
    accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame1_labelframe1_label5.grid(column=0,row=2,sticky='nw',pady=5,padx=[3,0])
    accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame1_labelframe1_equal3 = Label(accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame1_labelframe1, text=':', background=sub_lightdark, fg=text_color,font=('monogram',20))
    accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame1_labelframe1_equal3.grid(column=1,row=2,sticky='nw',pady=5)
    accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame1_labelframe1_label6 = Label(accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame1_labelframe1, text='Bing Bong', background=sub_lightdark, fg=text_color,font=('monogram',20))
    accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame1_labelframe1_label6.grid(column=2,row=2,sticky='nw',pady=5)

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
    accountingpage_subframe2_frame3_categorypage_leftframe_frame4.grid(column=1,row=2,sticky='nsew',padx=[0,3])

    accountingpage_subframe2_frame3_categorypage_leftframe_frame4_button1 = Button(accountingpage_subframe2_frame3_categorypage_leftframe_frame4,text='Add',foreground=text_color,background=light_dark,font=(custom_font,20,'bold'),command = lambda: to_button_page('add'))
    accountingpage_subframe2_frame3_categorypage_leftframe_frame4_button1.grid(column=0,row=0,sticky='nsew',pady=[3,3],padx=3,ipadx=30)

    accountingpage_subframe2_frame3_categorypage_leftframe_frame4_button2 = Button(accountingpage_subframe2_frame3_categorypage_leftframe_frame4,text='Remove',foreground=text_color,background=light_dark,font=(custom_font,20,'bold'),command = lambda: to_button_page('remove'))
    accountingpage_subframe2_frame3_categorypage_leftframe_frame4_button2.grid(column=0,row=1,sticky='nsew',pady=[0,3],padx=3,ipadx=30)

    accountingpage_subframe2_frame3_categorypage_leftframe_frame4_button3 = Button(accountingpage_subframe2_frame3_categorypage_leftframe_frame4,text='Edit',foreground=text_color,background=light_dark,font=(custom_font,20,'bold'),command = lambda: to_button_page('edit'))
    accountingpage_subframe2_frame3_categorypage_leftframe_frame4_button3.grid(column=0,row=2,sticky='nsew',pady=[0,3],padx=3,ipadx=30)

    accountingpage_subframe2_frame3_categorypage_leftframe_frame4_button4 = Button(accountingpage_subframe2_frame3_categorypage_leftframe_frame4,text='Search',foreground=text_color,background=light_dark,font=(custom_font,20,'bold'),command = lambda: to_button_page('search'))
    accountingpage_subframe2_frame3_categorypage_leftframe_frame4_button4.grid(column=0,row=3,sticky='nsew',pady=[0,3],padx=3,ipadx=30)

    # Right Frmae
    accountingpage_subframe2_frame3_categorypage_rightframe = Frame(accountingpage_subframe2_frame3_categorypage, background='blue')
    accountingpage_subframe2_frame3_categorypage_rightframe.grid(column=1,row=0,sticky='nsew')

    return accountingpage_subframe2_frame3_categorypage_leftframe_frame1_treeview, accountingpage_subframe2_frame3_categorypage_leftframe_frame3_frame1_labelframe1_label2

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

def validate_date(entry_widget,error_msg_widget):
    date_string = entry_widget.get()
    try:
        datetime.striptime(date_string, '%d-%m-%Y')
    except ValueError:
        error_msg_widget.configure(text='Invalid date format. Please use DD-MM-YYYY.')

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
    account TEXT PRIMARY KEY,
    account_type TEXT NOT NULL,
    transaction_count INTEGER DEFAULT 0,
    actual_value INTEGER DEFAULT 0,
 
    FOREIGN KEY (account_type) REFERENCES account_types(account_type)
    );
    '''
    cursor.execute(account_table)

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
    amount INTEGER NOT NULL,  
    FOREIGN KEY (from_account_type) REFERENCES account_types(account_type),
    FOREIGN KEY (from_account) REFERENCES accounts(account) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (to_account_type) REFERENCES account_types(account_type),
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
    END;
    '''
    update_trigger = '''
    CREATE TRIGGER IF NOT EXISTS update_summary_after_update
    AFTER UPDATE ON transactions
    BEGIN
        UPDATE accounts
        set actual_value = actual_value -
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
                WHEN NEW.from_account = NEW.to_account
                THEN 0
                ELSE 1
            END
        WHERE account = NEW.to_account;
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
    
app_startup()
print("Startup time:", time() - start_time, "seconds")
window.mainloop()
#load_page('accounting_page')