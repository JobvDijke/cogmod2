import ccm      
log=ccm.log(html=True)   

from ccm.lib.actr import *  

class myEnvironment(ccm.Model):        # items in the environment look and act like chunks - but note the syntactic differences
    diskLarge=ccm.Model(isa='diskLarge',location='counter1')
    diskMedium=ccm.Model(isa='diskMedium',location='diskLarge')
    diskSmall=ccm.Model(isa='diskSmall',location='diskMedium')

class myMotorModule(ccm.Model):
    def placeDiskSmallOnCounter3(self):
        print "place the small disk on the third counter"
        self.parent.parent.diskSmall.location = 'counter3'
        
    
    def placeDiskMediumOnCounter2(self):
        print "place the medium disk on the second counter"
        self.parent.parent.diskMedium.location = 'counter2'    
    
    def placeDiskSmallOnDiskMedium(self):
        print "place the small disk on the medium disk"
        self.parent.parent.diskSmall.location = 'diskMedium'
        
    def placeDiskLargeOnCounter3(self):
        print "place the large disk on the third counter"
        self.parent.parent.diskLarge.location = 'counter3'
        
    def placeDiskSmallOnCounter1(self):
        print "place the small disk on the first counter"
        self.parent.parent.diskSmall.location = 'counter1'
        
    def placeMediumDiskOnLargeDisk(self):
        print "place the medium disk on the large disk"
        self.parent.parent.diskMedium.location = 'diskLarge'

    
class myAgent(ACTR):
    focus = Buffer()
    motor = myMotorModule()
    
    def init():
        focus.set('smallDiskCounter3')
        
    def smallDiskStep1(focus='smallDiskCounter3'):
        print "I have a small disk"
        motor.placeDiskSmallOnCounter3()
        focus.set('mediumDiskCounter2')
        
    def mediumDiskStep2(focus='mediumDiskCounter2'):
        print "I have a medium disk"
        motor.placeDiskMediumOnCounter2()
        focus.set('smallDiskMediumDisk')
        
    def smallDiskStep3(focus='smallDiskMediumDisk', diskLarge='location:counter1'):
        print "I have a small disk"
        motor.placeDiskSmallOnDiskMedium()
        focus.set('largeDiskCounter3') 
        
    def largeDiskStep4(focus='largeDiskCounter3'):
        print "I have a large disk"
        motor.placeDiskLargeOnCounter3()
        focus.set('smallDiskCounter1')
    
    def smallDiskStep5(focus='smallDiskCounter1'):
        print "I have a small disk"
        motor.placeDiskSmallOnCounter1()
        focus.set('mediumDiskLargeDisk')
        
    def mediumDiskStep6(focus='mediumDiskLargeDisk'):
        print "I have a medium disk"
        motor.placeMediumDiskOnLargeDisk()
        focus.set('smallDiskMediumDisk')
            
    def smallDiskStep7(focus='smallDiskMediumDisk', diskLarge='location:counter3'):
        print "I have a small disk"
        motor.placeDiskSmallOnDiskMedium()
        focus.set('stop')
        
    def stop_production(focus='stop'):
        print "I am done"
        print "Small disk at: " + self.parent.diskSmall.location
        print "Medium disk at: " + self.parent.diskMedium.location
        print "Large disk at: " + self.parent.diskLarge.location
        self.stop()
    
environment = myEnvironment()
agent = myAgent()
environment.agent = agent
ccm.log_everything(environment)

environment.run()
ccm.finished()