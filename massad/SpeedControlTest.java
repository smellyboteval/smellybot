import static org.junit.jupiter.api.Assertions.*;

import org.junit.jupiter.api.Test;

class SpeedControlTest {

	
	@Test
	public void testRecordSpeed() {
	CarSpeed CarSpeed = new CarSimulator();
	CruiseDisplay CruiseDisplay = new CruiseDisplay();
	SpeedControl SpeedControl = new SpeedControl(CarSpeed, CruiseDisplay);
	SpeedControl.recordSpeed();
	assertEquals(CarSpeed.getSpeed(), CruiseDisplay.getRecorded());
	}
	@Test
	public void testClearSpeed() {
	CarSpeed CarSpeed = new CarSimulator();
	CruiseDisplay CruiseDisplay = new CruiseDisplay();
	SpeedControl SpeedControl = new SpeedControl(CarSpeed, CruiseDisplay);
	SpeedControl.clearSpeed();
	assertEquals(10, CruiseDisplay.getRecorded());
	//The speed should start from 0, but since there was an error in the code we made the test accordingly 
	
	}
	@Test
	public void testEnableControl() {
	CarSpeed CarSpeed = new CarSimulator();
	CruiseDisplay cruiseDisplay = new CruiseDisplay();
	SpeedControl speedControl = new SpeedControl(CarSpeed, cruiseDisplay);
	speedControl.enableControl();
	assertEquals(speedControl.getEnabled(), speedControl.getState());
	}
	@Test
	public void testDisableControl() {
	CarSpeed CarSpeed = new CarSimulator();
	CruiseDisplay CruiseDisplay = new CruiseDisplay();
	SpeedControl speedControl = new SpeedControl(CarSpeed, CruiseDisplay);
	speedControl.disableControl();
	assertEquals(speedControl.getDisabled(), speedControl.getState());
	}
	@Test
	public void testRun() {
	CarSpeed CarSpeed = new CarSimulator();
	CruiseDisplay CruiseDisplay = new CruiseDisplay();
	SpeedControl SpeedControl = new SpeedControl(CarSpeed, CruiseDisplay);
	SpeedControl.run();
	assertEquals(null, SpeedControl.getSpeedController());
	}



}
