package SWE316_HW.SWE316_HW;

import java.io.File;
import java.io.IOException;
import java.time.LocalDate;
import java.util.ArrayList;
import org.apache.poi.ss.usermodel.Sheet;
import org.apache.poi.ss.usermodel.Workbook;
import org.apache.poi.ss.usermodel.WorkbookFactory;

public class ExcelReader {

	private File excelFileProject;
	private Workbook wbProject;
	private File excelFileStages;
	private Workbook wbStages;
	private File excelFileStagesDetails;
	private Workbook wbStageDetails;
	private static int indicator = 1;
	private String nodeID;
	private String projectID;
	private int projectLastInt;
	private Sheet projSheet;
	private Sheet stageSheet;
	private Sheet stageDetailsSheet;
	private int stageNewVal;
	private int stageOldVal;
	private LocalDate date;

	public ExcelReader(String projectFileName, String stageFileName, String stageFileDetailsName) {
		try {
			excelFileProject = new File(projectFileName);
			wbProject = WorkbookFactory.create(excelFileProject);
			projSheet = wbProject.getSheetAt(0);

			excelFileStages = new File(stageFileName);
			wbStages = WorkbookFactory.create(excelFileStages);
			stageSheet = wbStages.getSheetAt(0);

			excelFileStagesDetails = new File(stageFileDetailsName);
			wbStageDetails = WorkbookFactory.create(excelFileStagesDetails);
			stageDetailsSheet = wbStageDetails.getSheetAt(0);
		} catch (IOException e) { // TODO remove
			e.printStackTrace();
		}
	}

	public ArrayList<Project> getProjects() {
		ArrayList<Project> projects = new ArrayList<Project>();
		for (int i = 1; i < projSheet.getPhysicalNumberOfRows(); i++) {
			projects.add(getProject(i));
		}
		return projects;
	}

	private Project getProject(int projIndex) {
		nodeID = projSheet.getRow(projIndex).getCell(0).toString();
		projectID = projSheet.getRow(projIndex).getCell(1).toString();
		projectLastInt = (int) Double.parseDouble(projSheet.getRow(projIndex).getCell(2).toString());
		return new Project(nodeID, projectID, getProjectStages(nodeID), projectLastInt);
	}

	private ArrayList<ProjectStage> getProjectStages(String nodeID) {
		ArrayList<ProjectStage> stages = new ArrayList<ProjectStage>();
		while (stageSheet.getPhysicalNumberOfRows() > indicator
				&& nodeID.equals(stageSheet.getRow(indicator).getCell(0).toString())) {
			stageNewVal = (int) Double.parseDouble(stageSheet.getRow(indicator).getCell(5).toString());
			stageOldVal = (int) Double.parseDouble(stageSheet.getRow(indicator).getCell(6) == null ? "0"
					: stageSheet.getRow(indicator).getCell(6).toString());
			date = stageDetailsSheet.getRow(indicator).getCell(2).getLocalDateTimeCellValue().toLocalDate();
			stages.add(new ProjectStage(stageOldVal, stageNewVal, date));
			indicator++;
		}
		return stages;
	}
}