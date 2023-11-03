package UserInterface;

import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.time.temporal.ChronoUnit;
import java.util.ArrayList;

import SWE316_HW.SWE316_HW.ProjectStage;
import javafx.geometry.Pos;
import javafx.scene.control.Label;
import javafx.scene.layout.Pane;
import javafx.scene.layout.Region;
import javafx.scene.paint.Color;
import javafx.scene.shape.Line;
import javafx.scene.shape.Rectangle;
import javafx.scene.text.TextAlignment;

public class TimeLiner extends Pane {
	// TODO maybe create manager class. SR Prin + if we need these fields for
	// another chart
	private double width;
	private ArrayList<ProjectStage> stages;
	private LocalDate projectStartDate;
	private LocalDate projectEndDate;
	private LocalDate lineStartDate;
	private LocalDate lineEndDate;

	private long daysToDraw;
	private double distanceBetweenDays;
	private final double stagesLineHeight = 300;

	public TimeLiner(double width, ArrayList<ProjectStage> stages) {
		this.stages = stages;
		this.width = width;	
		// TODO
		this.projectStartDate = stages.get(0).getDate();
		this.projectEndDate = stages.get(stages.size() - 1).getDate();
		this.lineStartDate = LocalDate.of(projectStartDate.getYear(), projectStartDate.getMonth(), 1);
		this.lineEndDate = LocalDate.of(projectEndDate.plusMonths(1).getYear(), projectEndDate.plusMonths(1).getMonth(),
				2);
		
		this.daysToDraw = ChronoUnit.DAYS.between(lineStartDate, lineEndDate);
		this.distanceBetweenDays = (double) width / daysToDraw;
		
		this.draw();
	}

	public void draw() {

		Line horizontalAxis = new Line(0, stagesLineHeight, width, stagesLineHeight);
		horizontalAxis.setStroke(Color.DARKGREY);
		horizontalAxis.setStrokeWidth(2);
		this.getChildren().add(horizontalAxis);

		LocalDate ithDate = lineStartDate;
		for (int i = 0; i < daysToDraw; i++, ithDate = ithDate.plusDays(1)) {
			double currentXPos = i * distanceBetweenDays;

			Line dayTickLine = new Line(currentXPos, stagesLineHeight - 3, currentXPos, stagesLineHeight);
			dayTickLine.setStroke(Color.DARKGREEN);

			if (ithDate.getDayOfMonth() == 1) {
				dayTickLine.setStrokeWidth(1.5);

				Label monthLabel = new Label();
				monthLabel.setText(ithDate.format(DateTimeFormatter.ofPattern("MMM")) + " " + ithDate.getYear());
				monthLabel.relocate(currentXPos - monthLabel.toString().length() / 2, stagesLineHeight);
				this.getChildren().add(monthLabel);
			} else {
				dayTickLine.setStrokeWidth(0.5);
			}

			// Check if the current day has a Project Stage
			int overlaps = 1;
			for (ProjectStage s : stages) {
				if (s.getDate().equals(ithDate)) {
					drawProjectStage(s, currentXPos, overlaps);
					overlaps++;
				}
			}

			this.getChildren().add(dayTickLine); // TODO
		}

		// Drawing The Duration Line

		// TODO maybe
		// if (showDuration == true) { ... // Checkbox in GUI
		drawDurationLine();

	}

	private void drawProjectStage(ProjectStage stage, double xPos, int overlaps) {
		Color color = stage.isModified() ? Color.RED : Color.GREEN;

		double y1Pos = stagesLineHeight;
		double y2Pos = y1Pos - (20 * overlaps);

		Line line = new Line(xPos, y1Pos, xPos, y2Pos);
		line.setStroke(Color.ORANGE);

		Label stageNumLabel = new Label(stage.getNewValue() + "");
		stageNumLabel.relocate(xPos + 6, y2Pos - 6);
		stageNumLabel.setTextFill(color);

		Rectangle square = new Rectangle(xPos, y2Pos, 5, 5);
		square.setFill(color);

		if (overlaps == 1) {
			String stageDate = stage.getDate().format(DateTimeFormatter.ofPattern("MM/dd/YYYY"));
			Label stageDateLabel = new Label(stageDate);
			stageDateLabel.relocate(xPos - stageDate.length(), y1Pos + 20);
			stageDateLabel.setTextFill(color);
			this.getChildren().add(stageDateLabel);
		}

		this.getChildren().addAll(line, square, stageNumLabel);
	}

	private void drawDurationLine() {
		double firstStageXPos = ChronoUnit.DAYS.between(lineStartDate, projectStartDate) * distanceBetweenDays;
		double finalStageXPos = ChronoUnit.DAYS.between(lineStartDate, projectEndDate) * distanceBetweenDays;

		Line p1 = new Line(firstStageXPos, 0 / 2, firstStageXPos, 0 / 2 - 30);
		Line p2 = new Line(finalStageXPos, 0 / 2, finalStageXPos, 0 / 2 - 30);

	}

}
