## Simple config to dictionnary converter
## You should use d_conf.get() to get a default value
## if the dictionnary does not contain required value

def ReadConf(filename):
    f_conf = open(filename, 'r')                # Open the conf file in Read Only
    d_conf = {}                                 # Create an empty dic

    for i in f_conf:                            # For each line
        i = i.strip()                           # Remove the '\n and spaces'
        if i and i[0] != '#':                   # If the string is not empty and it's not a comment
            s = i.split('=')
            key = s[0].strip()
            value = s[1].strip()
            d_conf[key] = value                 # Add the key to the dic

    return d_conf
