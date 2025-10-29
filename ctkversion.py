import tkinter as tk
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import customtkinter as ctk
from customtkinter import filedialog
import pandas as pd
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import ttk
from PIL import Image
import sqlite3

btnState = False
# Creation of the main window
class Main(ctk.CTkFrame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()

    # Method for creating the main window
    def init_main(self):
        my_font = ctk.CTkFont(family="san-francisco")

        #Creates an animatation for the navigation bar
        def switch():
            global btnState
            if btnState is True:
                for x in range(55, 251):
                    navRoot.place(x= -x, y= 0)
                    toolbar.update()

                btnState = False
            else:
                for x in range(-250, -55):
                    navRoot.place(x= x, y= 0)
                    toolbar.update()
                   
                btnState = True

        menu_ico = ctk.CTkImage(dark_image= Image.open('C:/Users/user/Documents/Documents/Python/Econometrics/material-symbols-light_menu-rounded.png'), size=(30,30))
        x_ico = ctk.CTkImage(dark_image= Image.open('C:/Users/user/Documents/Documents/Python/Econometrics/material-symbols-light_close-small-rounded.png'), size= (30,30))
        search_ico = ctk.CTkImage(dark_image= Image.open('C:/Users/user/Documents/Documents/Python/Econometrics/material-symbols-light_search-rounded.png'), size= (30,30))
        delete_ico = ctk.CTkImage(dark_image= Image.open('C:/Users/user/Documents/Documents/Python/Econometrics/material-symbols-light_delete-outline.png'), size= (30, 30))
        refresh_ico = ctk.CTkImage(dark_image= Image.open('C:/Users/user/Documents/Documents/Python/Econometrics/material-symbols-light_refresh.png'), size= (30,30))

        toolbar = ctk.CTkFrame(root, height= 650, width= 50)
        toolbar.pack(side=ctk.LEFT, fill=ctk.Y)

        navBar = ctk.CTkButton(toolbar, image=menu_ico, text="", fg_color="transparent",  command= switch)
        navBar.place(x= -45, y= 10)

        navRoot = ctk.CTkFrame(root, height= 650)
        navRoot.place(x= -250, y= 0)

        ctk.CTkButton(navRoot, text= "Create a file", font= my_font, fg_color= "aquamarine4", border_color= "dark", corner_radius=8.5, command=self.create_excel).place(x= 60, y= 100)

        ctk.CTkButton(navRoot, text= "Add a file", font= my_font, fg_color= "aquamarine4", border_color= "dark", corner_radius=8.5, command=self.open_dialog).place(x= 60, y= 135)

        ctk.CTkButton(navRoot, text= "Create a plot", font= my_font, fg_color= "aquamarine4", border_color= "dark", corner_radius=8.5, command=self.create).place(x= 60, y= 170)

        ctk.CTkButton(navRoot, text= "Edit", font= my_font, fg_color= "aquamarine4", border_color= "dark", corner_radius=8.5, command=self.open_edit).place(x= 60, y= 205)

        ctk.CTkButton(navRoot, text="Linear regression", font=my_font, fg_color="aquamarine4", corner_radius=8.5, command=self.run_linear_regression).place(x=60, y=240)

        ctk.CTkButton(navRoot, text="Polynomial regression", font=my_font, fg_color="aquamarine4", corner_radius=8.5, command=self.poly_regression).place(x=60, y=275)

        ctk.CTkButton(navRoot, text="Random forest", font=my_font, fg_color="aquamarine4", corner_radius=8.5, command=self.forest_regression).place(x=60, y=310)

        ctk.CTkButton(toolbar, image=search_ico, text="", fg_color="transparent", command=self.open_search).place(x= -45, y= 50)

        ctk.CTkButton(toolbar, image=refresh_ico, text="", fg_color="transparent", command=self.view_records).place(x= -45, y= 95)

        ctk.CTkButton(toolbar, image=delete_ico, text="", fg_color="transparent", command=self.delete_records).place(x= -45, y= 140)


        closeBtn = ctk.CTkButton(navRoot, image=x_ico, text="", fg_color="transparent", width= 30, command= switch)
        closeBtn.place(x= 150, y= 10)

        style = ttk.Style()
        style.theme_use("clam")     
        style.configure(
            "Custom.Treeview",
            background= "grey38",
            foreground= "grey97",
            font= my_font
        )   
        style.layout("Custom.Treeview", [
            ('Custom.Treeview', {'sticky': 'nswe'}),
            ("Custom.Treeview", {'sticky': 'nswe'}),
            ("Custom.Treeview", {'sticky':'nswe', 'children': [
                ("Custom.Treeview", {'sticky':'nswe', 'children': [
                    ("Custom.Treeview", {'side':'right', 'sticky':''}),
                    ("Custom.Treeview", {'sticky':'we'}),
                ]})
            ]}),]
        )
        style.map("Custom.Treeview", background= [('selected', 'aquamarine2')])

        self.tree = ttk.Treeview(root, columns=('id', 'month', 'revenue', 'income', 'prod_costs', 'indirect_costs', 'loan_percents', 'inc_tax', 'depreciation', 'path'), height=45, show='headings', style='Custom.Treeview')
        self.tree.pack(padx=150, ipadx= 500)

        self.tree.column('id', width=45, anchor=tk.CENTER)
        self.tree.column('month', width=150, anchor=tk.CENTER)
        self.tree.column('revenue', width=300, anchor=tk.CENTER)
        self.tree.column('income', width=150, anchor=tk.CENTER)
        self.tree.column('prod_costs', width=150, anchor=tk.CENTER)
        self.tree.column('indirect_costs', width=150, anchor=tk.CENTER)
        self.tree.column('loan_percents', width=150, anchor=tk.CENTER)
        self.tree.column('inc_tax', width=150, anchor=tk.CENTER)
        self.tree.column('depreciation', width=150, anchor=tk.CENTER)
        self.tree.column('path', width=150, anchor=tk.CENTER)

        self.tree.heading('id', text='id')
        self.tree.heading('month', text='Date')
        self.tree.heading('revenue', text='Revenue')
        self.tree.heading('income', text='Income')
        self.tree.heading('prod_costs', text='Production costs')
        self.tree.heading('indirect_costs', text='Indirect costs')
        self.tree.heading('loan_percents', text='Loan percents')
        self.tree.heading('inc_tax', text='Income tax')
        self.tree.heading('depreciation', text='Depreciation')
        self.tree.heading('path', text='Path')
        self.tree.pack(side=tk.LEFT)

        scroll = ctk.CTkScrollbar(root, command=self.tree.yview)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scroll.set)


    # Recording data method
    def records(self, month, revenue, income, prod_costs, indirect_costs, loan_percents, inc_tax, depreciation, path):
        self.db.insert_data(month, revenue, income, prod_costs, indirect_costs, loan_percents, inc_tax, depreciation, path)
        self.view_records()

    # Editing records from database method
    def edit_record(self, month, revenue, income, prod_costs, indirect_costs, loan_percents, inc_tax, depreciation, path):
        [ind], = db.cur.execute("""SELECT id FROM econometrics WHERE month LIKE ?""", ('%' + month + '%',))
        self.db.cur.execute('''
        UPDATE econometrics SET month = ?, revenue = ?, income = ?, prod_costs = ?, indirect_costs = ?, loan_percents = ?, inc_tax = ?, depreciation = ?, path =?
        WHERE id = ? ''', (month, revenue, income, prod_costs, indirect_costs, loan_percents, inc_tax, depreciation, path, int(ind)), )
        self.db.conn.commit()
        self.view_records()

    # Removing the highlighted stack in the table method
    def delete_records(self):
        for i in self.tree.selection():
            id = self.tree.set(i, '#1')
            self.db.cur.execute('''
            DELETE FROM econometrics
            WHERE id = ?
        ''', (id, ))
        self.db.conn.commit()
        self.view_records()

    # Search method by date
    def search_records(self, month):
        [self.tree.delete(i)  for i in self.tree.get_children()] 
        self.db.cur.execute("""SELECT * FROM econometrics WHERE month LIKE ?""", 
                            ('%' + month + '%',))
        [self.tree.insert('', 'end', values=i)  for i in self.db.cur.fetchall()]

    # Calls the creating an excel file method
    def create_excel(self):
        Creating_excel(root)

    # Calls the creating a boxplot method
    def create(self):
        Creating_boxplot(root)

    # Calls the additional window
    def open_dialog(self):
        Additional(root)

    # Calls the editing window
    def open_edit(self):
        Update()

    # Calls searching window
    def open_search(self):
        Search(root)

    # Calls the creating a polynomial regresssion method
    def poly_regression(self):
        Creating_poly_regression(root)

    # Calls the creating a random forest method
    def forest_regression(self):
        Creating_forest_regression(root)

    # Data visualization method
    def view_records(self):
        self.db.cur.execute("""SELECT * FROM econometrics""")
        [self.tree.delete(i)  for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=i)  for i in self.db.cur.fetchall()]

    # Creating a boxplot method
    def boxplotting(self, month):
        window = ctk.CTkToplevel(fg_color='black')
        window.title("Chart")
        window.geometry("1150x600")
        window.resizable(True, True)

        [filename], = db.cur.execute("""SELECT path FROM econometrics WHERE month LIKE ?""", ('%' + month + '%',))
        path = str(filename)
        df = pd.read_excel(path)
        df = df.assign(Income = df['Revenue'] - (df['Production_costs']+ df['Indirect_costs']+ df['Income_tax'] + df['Loan_percents'] + df['Depreciation']))
        fig = Figure(figsize=(35, 35), dpi=150)
        ax = fig.add_subplot(111) 

        labels = ['Revenue', 'Production\ncosts', 'Indirect\ncosts', 'Income tax', 'Loan \n percents', 'Depreciation', 'Income']
        red_circle = dict(markerfacecolor='teal', marker= 'o')
        mean_shape = dict(markerfacecolor='green', marker= '*')
        ax.set_facecolor('turquoise')
        ax.set_ylabel('Values (rub.)')


        ax.boxplot( df,
                    patch_artist=True,
                    vert=True,
                    flierprops=red_circle,
                    showmeans=True,
                    meanprops=mean_shape,
                    manage_ticks=True,
                    notch=False)
        ax.set_xticklabels(labels, fontsize= 5.5)


        canvas = FigureCanvasTkAgg(fig, master= window)
        canvas.draw()
        canvas.get_tk_widget().pack(side='top', fill=None, expand=0)
        window.after(200, None) 
    
    # Creating a linear regression method
    def run_linear_regression(self):
        df = pd.read_sql_query("SELECT * FROM econometrics", self.db.conn)

        X = df[['depreciation', 'prod_costs', 'indirect_costs']].values
        y = df['revenue'].values
        model = LinearRegression().fit(X, y)

        pred = model.predict(X)
        mse = mean_squared_error(y, pred)

        window = ctk.CTkToplevel(fg_color='black')
        window.title("Linear regression")
        window.geometry("700x500")

        fig, ax = plt.subplots(figsize=(8, 5))
        ax.scatter(y, pred, color='teal')
        ax.plot([y.min(), y.max()], [y.min(), y.max()], 'r--')
        ax.set_xlabel("Factual revenue")
        ax.set_ylabel("Predicted revenue")
        ax.set_title(f"Linear regression (MSE={mse:.2f})")

        canvas = FigureCanvasTkAgg(fig, master=window)
        canvas.draw()
        canvas.get_tk_widget().pack()

    # Creating a polynomial regression
    def run_polynomial_regression(self, degree0):
        df = pd.read_sql_query("SELECT * FROM econometrics", self.db.conn)

        degree = int(degree0)
        X = df[['depreciation', 'prod_costs', 'indirect_costs']].values
        y = df['revenue'].values

        poly = PolynomialFeatures(degree=degree)
        X_poly = poly.fit_transform(X)
        model = LinearRegression().fit(X_poly, y)
        pred = model.predict(X_poly)
        mse = mean_squared_error(y, pred)

        window = ctk.CTkToplevel(fg_color='black')
        window.title(f"Polynomial regression (degree={degree})")
        window.geometry("700x500")

        fig, ax = plt.subplots(figsize=(8, 5))
        ax.scatter(y, pred, color='orange')
        ax.plot([y.min(), y.max()], [y.min(), y.max()], 'r--')
        ax.set_xlabel("Factual revenue")
        ax.set_ylabel("Predicted revenue")
        ax.set_title(f"Polynomial regression (MSE={mse:.2f})")

        canvas = FigureCanvasTkAgg(fig, master=window)
        canvas.draw()
        canvas.get_tk_widget().pack()

    # Creating a random forest method
    def run_random_forest(self, trees):
        df = pd.read_sql_query("SELECT * FROM econometrics", self.db.conn)

        n_estimators = int(trees)
        X = df[['depreciation', 'prod_costs', 'indirect_costs']].values
        y = df['revenue'].values

        model = RandomForestRegressor(n_estimators=n_estimators, random_state=42)
        model.fit(X, y)
        pred = model.predict(X)
        mse = mean_squared_error(y, pred)

        window = ctk.CTkToplevel(fg_color='black')
        window.title(f"Random forest (n={n_estimators})")
        window.geometry("700x500")

        fig, ax = plt.subplots(figsize=(8, 5))
        ax.scatter(y, pred, color='limegreen')
        ax.plot([y.min(), y.max()], [y.min(), y.max()], 'r--')
        ax.set_xlabel("Factual revenue")
        ax.set_ylabel("Predicted revenue")
        ax.set_title(f"Random forest (MSE={mse:.2f})")

        canvas = FigureCanvasTkAgg(fig, master=window)
        canvas.draw()
        canvas.get_tk_widget().pack()


    # Creaating an excel file method
    def creating_xlsx(self, data, naming, revenue, prod_costs, indirect_costs, loan_percents, inc_tax, depreciation, entries, flag=0):
        inp = [revenue, prod_costs, indirect_costs, loan_percents, inc_tax, depreciation]
        nammings = ['Revenue', 'Production_costs', 'Indirect_costs', 'Income_tax', 'Loan_percents', 'Depreciation']
        
        for i in range(len(data)):
            data[nammings[i]].append(inp[i])
        df = pd.DataFrame(data)
        if flag:
            df.to_excel(naming, index=False)

        for entry in entries:
            entry.delete(0, 'end')
        




# Creation of the additional window
class Additional(ctk.CTkToplevel):
    def __init__(self, root):
        super().__init__(root)
        self.init_additional()
        self.view = app
        

    def init_additional(self):
        my_font = ctk.CTkFont(family="san-francisco")
        self.title('Addding information by date')
        self.geometry('450x200')
        self.attributes('-topmost' , 1)
        self.resizable(False, False)
        self.grab_set()
        self.focus_set()

        filename = filedialog.askopenfilename(title="Select file", filetype=(("Excel", "*.xlsx"), ("Excel", "*.xls"), ("Excel", "*.csv")))
        path = filename 
        df = pd.read_excel(path)
        df = df.assign(Income = df['Revenue'] - (df['Production_costs']+ df['Indirect_costs']+ df['Income_tax'] + df['Loan_percents'] + df['Depreciation']))
        label_month = ctk.CTkLabel(self, text='Month')
        label_month.place(x=50, y=50)

        self.entry_month = ctk.CTkEntry(self)
        self.entry_month.place(x=200, y=50)
        self.entry_revenue = int(df['Revenue'].sum()) 
        self.entry_income = int(df['Income'].sum())
        self.entry_prod_costs = int(df['Production_costs'].sum())
        self.entry_indirect_costs = int(df['Indirect_costs'].sum())
        self.entry_loan_percents = int(df['Loan_percents'].sum())
        self.entry_inc_tax = int(df['Income_tax'].sum())
        self.entry_depreciation = int(df['Depreciation'].sum())
        self.entry_path = path

        self.btn_ok = ctk.CTkButton(self, text='Add', font= my_font, fg_color= "aquamarine4", border_color= "dark",width= 80, corner_radius=8.5)
        self.btn_ok.bind('<Button-1>', lambda ev: self.view.records(self.entry_month.get(),
                                                                    self.entry_revenue,
                                                                    self.entry_income, 
                                                                    self.entry_indirect_costs,
                                                                    self.entry_prod_costs,
                                                                    self.entry_loan_percents,
                                                                    self.entry_inc_tax,
                                                                    self.entry_depreciation,
                                                                    self.entry_path))
        self.btn_ok.place(x=230, y=160)             

        btn_cancel = ctk.CTkButton(self, text='Close', font= my_font, fg_color= "aquamarine4", border_color= "dark", corner_radius=8.5, width= 80, command=self.destroy)
        btn_cancel.place(x=120, y=160)  

# Creation of the editing window
class Update(Additional):
    def __init__(self):
        super().__init__(root)
        self.db = db
        self.init_edit()


    def init_edit(self):
        my_font = ctk.CTkFont(family="san-francisco")
        self.title('Changing current information')
        self.btn_ok.destroy()
        self.btn_ok = ctk.CTkButton(self, text='Edit', font= my_font, fg_color= "aquamarine4", border_color= "dark", width= 80, corner_radius=8.5)
        self.btn_ok.bind('<Button-1>', 
                         lambda ev: self.view.edit_record(
                            self.entry_month.get(),
                            self.entry_revenue,
                            self.entry_income, 
                            self.entry_prod_costs,
                            self.entry_indirect_costs,
                            self.entry_loan_percents,
                            self.entry_inc_tax,
                            self.entry_depreciation,
                            self.entry_path))
        self.btn_ok.bind('<Button-1>', lambda ev: self.destroy(), add='+')
        self.btn_ok.place(x=210, y=160)   


#  Creation of the searching window
class Search(ctk.CTkToplevel):
    def __init__(self, root):
        super().__init__(root)
        self.init_search()
        self.view = app


    def init_search(self):
        my_font = ctk.CTkFont(family="san-francisco")
        self.title('Search by date')
        self.attributes('-topmost' , 1)
        self.geometry('300x130')
        self.resizable(False, False)
        self.grab_set()
        self.focus_set()

        label_month = ctk.CTkLabel(self, text='Date')
        label_month.place(x=25, y=30)
    
        self.entry_month = ctk.CTkEntry(self)
        self.entry_month.place(x=120, y=30)

        self.btn_ok = ctk.CTkButton(self, text='Find', font= my_font, fg_color= "aquamarine4", width=70, border_color= "dark", corner_radius=8.5)
        self.btn_ok.bind('<Button-1>', lambda ev: self.view.search_records(self.entry_month.get()))
        self.btn_ok.bind('<Button-1>', lambda ev: self.destroy(), add='+')
        self.btn_ok.place(x=125, y=90)             

        btn_cancel = ctk.CTkButton(self, text='Close',font= my_font, fg_color= "aquamarine4", width=25, border_color= "dark", corner_radius=8.5, command=self.destroy)
        btn_cancel.place(x=50, y=90)  


# Creation of the boxplot window
class Creating_boxplot(ctk.CTkToplevel):
    def __init__(self, root):
        super().__init__(root)
        self.db = db
        self.init_creating()
        self.view = app

    def init_creating(self):
        my_font = ctk.CTkFont(family="san-francisco")
        self.title('Creating a chart')
        self.attributes('-topmost' , 1)
        self.geometry('300x125')    
        self.resizable(False, False)
        self.grab_set()
        self.focus_set()

        label_month = ctk.CTkLabel(self, text='Date')
        label_month.place(x=50, y=30)
        label_month.pack(anchor='nw', padx=6, pady=6)
    
        self.entry_month = ctk.CTkEntry(self)
        self.entry_month.place(x=150, y=30)
        self.entry_month.pack(anchor='nw', padx=6, pady=6)
        
        self.btn_ok = ctk.CTkButton(self, text='Create', font= my_font, fg_color= "aquamarine4", border_color= "dark", width= 80, corner_radius=8.5)
        self.btn_ok.bind('<Button-1>', lambda ev: self.view.boxplotting(self.entry_month.get()))
        self.btn_ok.place(x=180, y=95) 

        btn_cancel = ctk.CTkButton(self, text='Close', font= my_font, fg_color= "aquamarine4", border_color= "dark", corner_radius=8.5, width= 80, command=self.destroy)
        btn_cancel.place(x=90, y=95) 




# Creation of the polynomial regression window
class Creating_poly_regression(ctk.CTkToplevel):
    def __init__(self, root):
        super().__init__(root)
        self.db = db
        self.init_poly()
        self.view = app

    #
    def init_poly(self):
        my_font = ctk.CTkFont(family="san-francisco")
        self.title('Polynomial regression')
        self.attributes('-topmost', 1)
        self.geometry('300x150')
        self.resizable(False, False)
        self.grab_set()
        self.focus_set()

        label_degree = ctk.CTkLabel(self, text='Polynomial degree:')
        label_degree.place(x=30, y=30)

        self.entry_degree = ctk.CTkEntry(self)
        self.entry_degree.insert(0, "2")
        self.entry_degree.place(x=150, y=30)

        self.btn_ok = ctk.CTkButton(self, text='Create', font= my_font, fg_color= "aquamarine4", border_color= "dark", width= 80, corner_radius=8.5)
        self.btn_ok.bind('<Button-1>', lambda ev: self.view.run_polynomial_regression(self.entry_degree.get()))
        self.btn_ok.place(x=180, y=95) 

        btn_cancel = ctk.CTkButton(self, text='Close', font= my_font, fg_color= "aquamarine4", border_color= "dark", corner_radius=8.5, width= 80, command=self.destroy)
        btn_cancel.place(x=90, y=95) 


# Creation of the random forest window
class Creating_forest_regression(ctk.CTkToplevel):
    def __init__(self, root):
        super().__init__(root)
        self.db = db
        self.init_forest()
        self.view = app

    def init_forest(self):
        my_font = ctk.CTkFont(family="san-francisco")
        self.title('Regression of the random forest')
        self.attributes('-topmost', 1)
        self.geometry('300x150')
        self.resizable(False, False)
        self.grab_set()
        self.focus_set()

        label_trees = ctk.CTkLabel(self, text='Number of trees:')
        label_trees.place(x=50, y=30)

        self.entry_trees = ctk.CTkEntry(self)
        self.entry_trees.insert(0, "100")
        self.entry_trees.place(x=150, y=30)

        self.btn_ok = ctk.CTkButton(self, text='Create', font= my_font, fg_color= "aquamarine4", border_color= "dark", width= 80, corner_radius=8.5)
        self.btn_ok.bind('<Button-1>', lambda ev: self.view.run_random_forest(self.entry_trees.get()))
        self.btn_ok.place(x=180, y=95) 

        btn_cancel = ctk.CTkButton(self, text='Close', font= my_font, fg_color= "aquamarine4", border_color= "dark", corner_radius=8.5, width= 80, command=self.destroy)
        btn_cancel.place(x=90, y=95) 

    
#  Creation of the excel window
class Creating_excel(ctk.CTkToplevel):
    def __init__(self, root):
        super().__init__(root)
        self.db = db
        self.init_creating()
        self.view = app

    def init_creating(self):
        my_font = ctk.CTkFont(family="san-francisco")
        self.title('Data entry')
        self.attributes('-topmost' , 1)
        self.geometry('330x405')    
        self.resizable(False, False)
        self.grab_set()
        self.focus_set()


        label_naming = ctk.CTkLabel(self, text='File\nname')
        label_naming.place(x=30, y=30)
        label_revenue = ctk.CTkLabel(self, text='Revenue')
        label_revenue.place(x=25, y=80)
        label_prod_costs = ctk.CTkLabel(self, text='Production\ncosts')
        label_prod_costs.place(x=20, y=130)
        label_indirect_costs = ctk.CTkLabel(self, text='Indirect\ncosts')
        label_indirect_costs.place(x=30, y=180)
        label_loan_percents = ctk.CTkLabel(self, text='Loan\npercents')
        label_loan_percents.place(x=30, y=230)
        label_inc_tax = ctk.CTkLabel(self, text='Income\ntax')
        label_inc_tax.place(x=30, y=280)
        label_depreciation = ctk.CTkLabel(self, text='Depreciation')
        label_depreciation.place(x=30, y=330)
    
        self.entry_naming = ctk.CTkEntry(self)
        self.entry_naming.place(x=180, y=30)
        self.entry_revenue = ctk.CTkEntry(self)
        self.entry_revenue.place(x=180, y=80)
        self.entry_prod_costs = ctk.CTkEntry(self)
        self.entry_prod_costs.place(x=180, y=130)
        self.entry_indirect_costs = ctk.CTkEntry(self)
        self.entry_indirect_costs.place(x=180, y=180)
        self.entry_loan_percents = ctk.CTkEntry(self)
        self.entry_loan_percents.place(x=180, y=230)
        self.entry_inc_tax = ctk.CTkEntry(self)
        self.entry_inc_tax.place(x=180, y=280)
        self.entry_depreciation = ctk.CTkEntry(self)
        self.entry_depreciation.place(x=180, y=330)


        # Creating a dictionary with lists that will be used when creating excel files
        data = {
                    'Revenue': [],  
                    'Production_costs': [],
                    'Indirect_costs': [],
                    'Income_tax': [],
                    'Loan_percents': [],
                    'Depreciation': []
                }

        entries = [self.entry_revenue, self.entry_prod_costs, self.entry_indirect_costs, self.entry_loan_percents, self.entry_inc_tax, self.entry_depreciation]

        self.btn_ok = ctk.CTkButton(self, text='Entry', font= my_font, fg_color= "aquamarine4", width= 80 ,border_color= "dark", corner_radius=8.5)
        self.btn_ok.bind('<Button-1>', lambda ev: self.view.creating_xlsx(
                            data,
                            self.entry_naming.get(),
                            int(self.entry_revenue.get()), 
                            int(self.entry_prod_costs.get()),
                            int(self.entry_indirect_costs.get()),
                            int(self.entry_loan_percents.get()),
                            int(self.entry_inc_tax.get()),
                            int(self.entry_depreciation.get()), entries))
        self.btn_ok.place(x=225, y=370) 
        self.btn_create = ctk.CTkButton(self, text='Create', font= my_font, fg_color= "aquamarine4", width= 80 ,border_color= "dark", corner_radius=8.5)
        self.btn_create.bind('<Button-1>', lambda ev: self.view.creating_xlsx(
                            data,
                            self.entry_naming.get(),
                            int(self.entry_revenue.get()), 
                            int(self.entry_prod_costs.get()),
                            int(self.entry_indirect_costs.get()),
                            int(self.entry_loan_percents.get()),
                            int(self.entry_inc_tax.get()),
                            int(self.entry_depreciation.get()), entries, 1))
        self.btn_create.place(x=135, y=370) 

        btn_cancel = ctk.CTkButton(self, text='Close',font= my_font, fg_color= "aquamarine4", border_color= "dark", width= 80 ,corner_radius=8.5, command=self.destroy)
        btn_cancel.place(x=45, y=370) 


# Database creation
class Db():
    def __init__(self):
        self.conn = sqlite3.connect('info.db')
        self.cur = self.conn.cursor()
        self.cur.execute ('''
                CREATE TABLE IF NOT EXISTS econometrics (
                        id INTEGER PRIMARY KEY,
                        month TEXT,
                        revenue INTEGER,
                        income INTEGER,
                        prod_costs INTEGER,
                        indirect_costs INTEGER,
                        loan_percents INTEGER,
                        inc_tax INTEGER,
                        depreciation INTEGER,
                        path TEXT  
                )''')
        

    def insert_data(self, month, revenue, income, prod_costs, indirect_costs, loan_percents, inc_tax, depreciation, path):
        self.cur.execute('''
        INSERT INTO econometrics (month, revenue, income, prod_costs, indirect_costs, loan_percents, inc_tax, depreciation, path)
                         VALUES (?,?,?,?,?,?,?,?,?)''', (month, revenue, income, prod_costs, indirect_costs, loan_percents, inc_tax, depreciation, path))
        self.conn.commit()



if __name__ == '__main__':
    root = ctk.CTk()
    db = Db()
    app = Main(root)
    app.pack()
    ctk.set_appearance_mode('dark')
    root.title('Econometrics')
    root.geometry('1215x650')
    root.resizable(True, True)
    root.mainloop()

