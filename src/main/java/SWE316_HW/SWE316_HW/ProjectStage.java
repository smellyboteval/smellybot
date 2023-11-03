package SWE316_HW.SWE316_HW;

import java.time.LocalDate;

public class ProjectStage {
	private int oldValue, newValue;
	private LocalDate date;

	public ProjectStage(int oldValue, int newValue, LocalDate date) {
		this.oldValue = oldValue;
		this.newValue = newValue;
		this.date = date;
	}

	public int getOldValue() {
		return oldValue;
	}

	public int getNewValue() {
		return newValue;
	}

	public LocalDate getDate() {
		return date;
	}

	public void setOldValue(int oldValue) {
		this.oldValue = oldValue;
	}

	public void setNewValue(int newValue) {
		this.newValue = newValue;
	}

	public void setDate(LocalDate date) {
		this.date = date;
	}

	public boolean isModified() {
		return newValue < oldValue;
	}

	@Override
	public String toString() {
		return String.format("Old Value: %d, New Value: %d, Date: %s\n", this.getOldValue(), this.getNewValue(),
				this.getDate());
	}

}
