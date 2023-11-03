package UserInterface;

import java.util.ArrayList;

import SWE316_HW.SWE316_HW.ExcelReader;
import SWE316_HW.SWE316_HW.Project;
import javafx.application.Application;
import javafx.geometry.Pos;
import javafx.scene.Scene;
import javafx.scene.control.Label;
import javafx.scene.layout.BorderPane;
import javafx.scene.layout.HBox;
import javafx.scene.layout.VBox;
import javafx.stage.Stage;

public class GUI extends Application {

	ExcelReader excelReader = new ExcelReader("Projects.xls", "Stages.xls", "Stages_Detailed.xls");

	@Override
	public void start(Stage primaryStage) {

//		TimeLiner timeline = new TimeLiner(500, new String[] { "Event 1", null, null, "Event 2", null, "Event 3",
//				"Event 4", null, null, null, "Event 5" });

		BorderPane mainPane = new BorderPane();
		mainPane.setStyle("-fx-background-color: #e2eeff");

//		ArrayList<Project> x = new ArrayList<>();
//		x.add(new Project("123", "123", null, 1));
//		x.add(new Project("4312", "234", null, 2));
//		x.add(new Project("156423", "345", null, 3));
//		x.add(new Project("1423", "456", null, 4));
//		
//		ArrayList<ProjectStage> sts = new ArrayList<>();
//		sts.add(new ProjectStage(0, 1, LocalDate.of(2022, 2, 3)));
//		sts.add(new ProjectStage(1, 2, LocalDate.of(2022, 3, 5)));
//		sts.add(new ProjectStage(2, 3, LocalDate.of(2022, 7, 7)));

		ArrayList<Project> projectsList = excelReader.getProjects();
		ProjectListBox projectListBox = new ProjectListBox(projectsList);

		mainPane.setLeft(projectListBox);
		mainPane.setCenter(new Label("Select A Project"));

		// TODO
		projectListBox.getSelectionModel().selectedItemProperty().addListener(e -> {
			Project selectedProject = projectListBox.getSelectionModel().getSelectedItem();
			mainPane.setTop(new Label("Project ID: " + selectedProject.getProjectID()));

			System.out.println(selectedProject.getStages());
			TimeLiner timeliner = new TimeLiner(mainPane.getWidth() * 0.75, selectedProject.getStages());

			HBox hb = new HBox(timeliner);
			hb.setAlignment(Pos.CENTER);
			VBox vb = new VBox(hb);
			vb.setAlignment(Pos.CENTER);
			mainPane.setCenter(vb);

//			mainPane.setCenter(timeliner);
		});

//		HBox hb = new HBox();
//		hb.setAlignment(Pos.CENTER);
//		VBox vb = new VBox(hb);
//		vb.setAlignment(Pos.CENTER);

		Scene scene = new Scene(mainPane, 1500, 680);
		primaryStage.setTitle("Project Timeliner");
		primaryStage.setScene(scene);
		primaryStage.show();
	}

}
