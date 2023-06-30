from website import create_app

app = create_app() #used to create an instance or initialize it 

if __name__ == '__main__': 
    app.run(debug=True)

