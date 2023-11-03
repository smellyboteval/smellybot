
class Controller {
  final static int INACTIVE = 0; // cruise controller states
  final static int ACTIVE   = 1;
  final static int CRUISING = 2;
  final static int STANDBY  = 3;
  private int controlState  = INACTIVE; //initial state
  private SpeedControl sc;
  private boolean isfixed;

  Controller(CarSpeed cs, CruiseDisplay disp, boolean b)
    {sc=new SpeedControl(cs,disp); isfixed=b;}

  synchronized void brake(){
    if (controlState==CRUISING )
      {controlState=STANDBY; }
  }

  synchronized void accelerator(){
    if (controlState==CRUISING )
      {sc.disableControl(); controlState=STANDBY; }
  }

  synchronized void engineOff(){
    if(controlState!=INACTIVE) {
      if (isfixed) sc.disableControl(); 
      controlState=INACTIVE;
    }
  }

  synchronized void engineOn(){
    if(controlState==INACTIVE)
      {sc.clearSpeed(); controlState=ACTIVE;}
  }

  synchronized void on(){
    if(controlState!=INACTIVE){
      sc.recordSpeed(); sc.enableControl();
      controlState=CRUISING;
    }
  }

  synchronized void off(){
    if(controlState==CRUISING )
      {sc.disableControl(); controlState=STANDBY;}
    else {
       controlState=INACTIVE;
       sc.disableControl();
    }
  }

  synchronized void resume(){
    if(controlState==STANDBY)
     {sc.enableControl(); controlState=CRUISING;}
  }

public int getControlState() {
	return controlState;
}

public void setControlState(int controlState) {
	this.controlState = controlState;
}

public SpeedControl getSc() {
	return sc;
}

public void setSc(SpeedControl sc) {
	this.sc = sc;
}

public boolean isIsfixed() {
	return isfixed;
}

public void setIsfixed(boolean isfixed) {
	this.isfixed = isfixed;
}

public static int getInactive() {
	return INACTIVE;
}

public static int getActive() {
	return ACTIVE;
}

public static int getCruising() {
	return CRUISING;
}

public static int getStandby() {
	return STANDBY;
}
}

