import random
class NameAI:
    """
    Try to create first librry

    Example
    # -------------------
    uncle = NameAI()
    uncle.show_name()
    uncle.show_youtube()
    uncle.about()
    uncle.show_art()
    # -------------------
    """

    def __init__(self):
        self.name = 'Happy'
        self.page = 'www.facebook.com'

    def show_name(self):
        print('สวัสดีฉันชื่อ {}'.format(self.name))

    def show_youtube(self):
        print('www.youtube.com')

    def about(self):
        text = """
        สวัสดีครับนี่คือผมเอง 'Name AI'
        """
        print(text)

    def show_art(self):
        text ="""
                                                ^^
            ^^      ..                                       ..
                    []                                       []
                  .:[]:_          ^^                       ,:[]:.
                .: :[]: :-.                             ,-: :[]: :.
              .: : :[]: : :`._                       ,.': : :[]: : :.
            .: : : :[]: : : : :-._               _,-: : : : :[]: : : :.
        _..: : : : :[]: : : : : : :-._________.-: : : : : : :[]: : : : :-._
        _:_:_:_:_:_:[]:_:_:_:_:_:_:_:_:_:_:_:_:_:_:_:_:_:_:_:[]:_:_:_:_:_:_
        !!!!!!!!!!!![]!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!![]!!!!!!!!!!!!!
        ^^^^^^^^^^^^[]^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^[]^^^^^^^^^^^^^
                    []                                       []
                    []                                       []
                    []                                       []
        ~~^-~^_~^~/  \~^-~^~_~^-~_^~-^~_^~~-^~_~^~-~_~-^~_^/  \~^-~_~^-~~-
        ~ _~~- ~^-^~-^~~- ^~_^-^~~_ -~^_ -~_-~~^- _~~_~-^_ ~^-^~~-_^-~ ~^
        ~ ^- _~~_-  ~~ _ ~  ^~  - ~~^ _ -  ^~-  ~ _  ~~^  - ~_   - ~^_~
            ~-  ^_  ~^ -  ^~ _ - ~^~ _   _~^~-  _ ~~^ - _ ~ - _ ~~^ -
        jgs     ~^ -_ ~^^ -_ ~ _ - _ ~^~-  _~ -_   ~- _ ~^ _ -  ~ ^-
                    ~^~ - _ ^ - ~~~ _ - _ ~-^ ~ __- ~_ - ~  ~^_-
                        ~ ~- ^~ -  ~^ -  ~ ^~ - ~~  ^~ - ~        
                
        """
        print(text)

    def dice(self):
        dice_list = ['1','2','3','4','5','6']
        first = random.choice(dice_list)
        second = random.choice(dice_list)
        print('คุณทอยเต๋าได้: {} {}'.format(first,second))

if __name__ == '__main__':
    uncle = NameAI()
    uncle.show_name()
    uncle.show_youtube()
    uncle.about()
    uncle.show_art()
    uncle.dice()