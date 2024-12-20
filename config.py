#WINDOW DIMENSIONS
INIT_WIDTH = 1366
INIT_HEIGHT = 768
TOP_FRAME_HEIGHT = 20
BOTTOM_FRAME_HEIGHT = INIT_HEIGHT - TOP_FRAME_HEIGHT
BUTTON_WIDTH = 20

#TOOL MODIFIABLES
SUPPORTED_FORMATS = ["jpg","png","jpeg","JPEG","tiff"]
TYPE_CHOICES = ["None", 
    "Printed Key", "Written Key", 
    "Printed Value", "Written Value",
    "Check Box Key", "Check Box Value",
    "Comment/Info", "Logo", 
    "Signature", "Photograph"
    ]
'''
TYPE_CHOICES = ["None",
    "ADDRESS",
    "NAME",
    "DOB",
    "GENDER",
    "AADHAAR",
    "MOBILE",
    "PHOTO",
    "BARCODE",
    "QR"
    ]
'''
FONT_SIZE = 11
ICON_NAME = 'icon.ico'
LOG_FILE = 'form_labeller.log'
LOGGING = True
DEBUGGING = True
ALLOWED_DEBUG_LEVEL = 3

#POINTS DIMENSIONS
RADIUS = 5
SMALL_RADIUS = 1
BIG_RADIUS = 5

#BUTTON POSITIONS
OPEN_FOLDER_ROW,OPEN_FOLDER_COL = 0,0
PREV_ROW,PREV_COL = 1,0
NEXT_ROW,NEXT_COL = 1,1
SAVE_ROW,SAVE_COL = 2,0
DEL_SELECTED_ROW,DEL_SELECTED_COL = 3,0
DROP_DOWN_ROW,DROP_DOWN_COL = 4,0
SAVE_TYPE_ROW,SAVE_TYPE_COL = 4,1
DESELECT_ALL_ROW,DESELECT_ALL_COL = 5,0
SELECT_ALL_ROW, SELECT_ALL_COL = 6,0
DRAW_POLY_ROW, DRAW_POLY_COL = 7,0
DRAW_RECT_ROW, DRAW_RECT_COL = 8,0
DELETE_ALL_ROW, DELETE_ALL_COL = 9,0
SHOW_TYPE_ROW,SHOW_TYPE_COL = 10,0
HIDE_TYPE_ROW,HIDE_TYPE_COL = 10,1
MAKE_TIGHT_ROW = 11
THRESHOLD_ROW = 12
LABEL_TEXT_ROW = 13
