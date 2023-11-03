

 class SpeedControl implements Runnable {
  final static int DISABLED = 0; //speed control states
  final static int ENABLED  = 1;
  volatile private int state = DISABLED;  //initial state
  volatile private int setSpeed = 0;      //target cruise control speed
  volatile private Thread speedController;
  volatile private CarSpeed cs;         //interface to control speed of engine
  volatile private CruiseDisplay disp;

  SpeedControl(CarSpeed cs, CruiseDisplay disp){
    this.cs=cs; this.disp=disp;
    disp.disabled(); disp.record(0);
  }

  synchronized void recordSpeed(){
    setSpeed=cs.getSpeed(); disp.record(setSpeed);
  }

  synchronized void clearSpeed(){
    if (state==DISABLED) {setSpeed=10;disp.record(setSpeed);}
  }

  synchronized void enableControl(){
    if (state==DISABLED) {
	  disp.enabled();
      speedController= new Thread(this);
      speedController.start();
      state=ENABLED;
    }
  }

  synchronized void disableControl(){
    if (state==ENABLED)  {disp.disabled(); state=DISABLED;}
  }

  synchronized public void run() {     // the speed controller thread
    try {
   	  while (state==ENABLED) {
		double error = (float)(setSpeed-cs.getSpeed())/6.0;
		double steady = (double)setSpeed/12.0;
		cs.setThrottle(steady+error); //simplified feed back control
	    wait(500);
      } 
    } catch (InterruptedException e) {}
    speedController=null;
  }

public int getState() {
	return state;
}

public void setState(int state) {
	this.state = state;
}

public int getSetSpeed() {
	return setSpeed;
}

public void setSetSpeed(int setSpeed) {
	this.setSpeed = setSpeed;
}

public Thread getSpeedController() {
	return speedController;
}

public void setSpeedController(Thread speedController) {
	this.speedController = speedController;
}

public CarSpeed getCs() {
	return cs;
}

public void setCs(CarSpeed cs) {
	this.cs = cs;
}

public CruiseDisplay getDisp() {
	return disp;
}

public void setDisp(CruiseDisplay disp) {
	this.disp = disp;
}

public static int getDisabled() {
	return DISABLED;
}

public static int getEnabled() {
	return ENABLED;
}
}





