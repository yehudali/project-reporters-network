import logging
import sys

class AppLogger:
    @staticmethod
    def get_logger(name: str):
        # 1. יצירת אובייקט הלוגר
        logger = logging.getLogger(name)
        
        # אם ללוגר כבר יש Handlers (כדי למנוע כפילויות בהדפסה)
        if not logger.handlers:
            logger.setLevel(logging.INFO) # קובע מאיזו רמה להדפיס

            # 2. יצירת ה-Handler (לאן הלוג הולך - כאן למסך)
            handler = logging.StreamHandler(sys.stdout)
            
            # 3. הגדרת הפורמט (איך השורה תיראה)
            # זמן | רמת חומרה | שם הרכיב | ההודעה
            formatter = logging.Formatter(
                '%(asctime)s | %(levelname)s | %(name)s | %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            handler.setFormatter(formatter)
            
            # חיבור ה-Handler ללוגר
            logger.addHandler(handler)
            
        return logger