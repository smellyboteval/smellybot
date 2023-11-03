package SWE316_HW.SWE316_HW;

import java.util.ArrayList;

public class Project {
	private String nodeID;
	private String projectID;
	private ArrayList<ProjectStage> stages;
	private int lastStage;

	public Project(String nodeID, String projectID, ArrayList<ProjectStage> stages, int lastStage) {
		this.nodeID = nodeID;
		this.projectID = projectID;
		this.stages = stages;
		this.lastStage = lastStage;
	}

	public String getNodeID() {
		return nodeID;
	}

	public String getProjectID() {
		return projectID;
	}

	public ArrayList<ProjectStage> getStages() {
		return stages;
	}

	public int getLastStage() {
		return lastStage;
	}

	public void setNodeID(String nodeID) {
		this.nodeID = nodeID;
	}

	public void setProjectID(String projectID) {
		this.projectID = projectID;
	}

	public void setStages(ArrayList<ProjectStage> stages) {
		this.stages = stages;
	}

	public void setLastStage(int lastStage) {
		this.lastStage = lastStage;
	}

}
