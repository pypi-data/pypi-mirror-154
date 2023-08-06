class myfirstmodule:
    def greet(name):
        """
        This function greets to
        the person passed in as
        a parameter
        """
        print("Hello, " + name + ". Good morning!")
    def absolute_value(num):
        """This function returns the absolute
        value of the entered number"""

        if num >= 0:
            return num
        else:
            return -num