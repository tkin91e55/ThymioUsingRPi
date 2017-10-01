def forward(thymioCtlr, speed):
    """
    Arguments:
        thymioCtlr (ThymioController)
        speed (int) : from 0 to 250
    """
    #a.TrigEvent("forward",[])
    thymioCtlr.SetVar("motor.left.target",[speed])
    thymioCtlr.SetVar("motor.right.target",[speed])

def backward(thymioCtlr, speed):
    """
    Arguments:
        thymioCtlr (ThymioController)
        speed (int) : from 0 to 250
    """
    #a.TrigEvent("forward",[])
    thymioCtlr.SetVar("motor.left.target",[-1 * speed])
    thymioCtlr.SetVar("motor.right.target",[-1 * speed])

def turnLeft(thymioCtlr, speed):
    """
    Arguments:
        thymioCtlr (ThymioController)
        speed (int) : from 0 to 250
    """
    #a.TrigEvent("forward",[])
    thymioCtlr.SetVar("motor.left.target",[-1 * speed])
    thymioCtlr.SetVar("motor.right.target",[speed])

def turnRight(thymioCtlr, speed):
    """
    Arguments:
        thymioCtlr (ThymioController)
        speed (int) : from 0 to 250
    """
    #a.TrigEvent("forward",[])
    thymioCtlr.SetVar("motor.left.target",[speed])
    thymioCtlr.SetVar("motor.right.target",[-1 * speed])

def test():
    print 'Hello'

from init import ThymioController

if __name__ == '__main__':
    ctlr = ThymioController("scripts/tmpl.aesl")
    forward(ctlr,0)



