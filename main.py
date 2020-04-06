from app import app
import view
from app import db

if __name__ == '__main__':
  
    app.run(host='0.0.0.0', debug=True, port=3306)