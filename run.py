from program_files import app
app.config['SECRET_KEY'] = 'any secret string'

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=33507, debug=True)
