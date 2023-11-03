package UserInterface;

import java.util.ArrayList;

import SWE316_HW.SWE316_HW.Project;
import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import javafx.scene.control.TableColumn;
import javafx.scene.control.TableView;
import javafx.scene.control.cell.PropertyValueFactory;

public class ProjectListBox extends TableView<Project> {

	public ProjectListBox(ArrayList<Project> projectsList) {

		// Creating the columns for Project ID and Stage
		TableColumn<Project, String> idColumn = new TableColumn<>("Project ID");
		TableColumn<Project, Integer> stageNumberColumn = new TableColumn<>("Stage");

		idColumn.setCellValueFactory(new PropertyValueFactory<>("projectID"));
		stageNumberColumn.setCellValueFactory(new PropertyValueFactory<>("lastStage"));

		ObservableList<Project> observableProjectsList = FXCollections.observableArrayList(projectsList);

		this.getColumns().addAll(idColumn, stageNumberColumn);
		this.setItems(observableProjectsList);
		this.setColumnResizePolicy(TableView.CONSTRAINED_RESIZE_POLICY);
	}

}
