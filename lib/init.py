
def init_server():
    init_commands()
    init_emotes()

def init_commands():
    
    cmdList = {}
    
    from glob import glob
    from os.path import split
    scripts = glob('cmds/' + '*.py')
    
    for script in scripts:
        try:
            execfile(script)
        except NameError:
            continue
      
        cmdClass = locals()['CmdObj']
        cmdName =  split(script)[-1][:-3]
        cmdList[cmdName] = cmdClass()
    import G
    G.CmdList = cmdList


def init_emotes():
    emotes = {}
    
    from glob import glob
    from os.path import split
    scripts = glob('cmds/emotes/' + '*.py')
    
    for script in scripts:
        try:
            execfile(script)
        except NameError:
            continue
        
        emoteClass = locals()['EmoteObj']
        emoteName =  split(script)[-1][:-3]
        emotes[emoteName] = emoteClass()
        
    G.EmoteList = emotes

