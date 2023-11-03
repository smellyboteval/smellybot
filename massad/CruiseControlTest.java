


import static org.junit.jupiter.api.Assertions.*;

import org.junit.jupiter.api.Test;

class CruiseControlTest {

	
	@Test
	public void stop() {



	CruiseControl cc = new CruiseControl();

	cc.getCar().engineOn() ;
	cc.getControl().engineOn();
	cc.stop();
	assertFalse(cc.getCar().isIgnition());
	assertEquals(cc.getControl().getInactive(), cc.getControl().getControlState());



	}
}
