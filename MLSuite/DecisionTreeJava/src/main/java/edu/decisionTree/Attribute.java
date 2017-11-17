package edu.decisionTree;

import java.io.Serializable;
import java.util.Set;

public class Attribute implements Serializable  {

	/**
	 * 
	 */
	private static final long serialVersionUID = 1L;
	private String name;
	private Set<String> values;
	private Double infoGain;
	private int number;
	private String majorityValue;

	public String getName() {
		return name;
	}
	public void setName(String name) {
		this.name = name;
	}
	public Set<String> getValues() {
		return values;
	}
	public void setValues(Set<String> values) {
		this.values = values;
	}
	public Double getInfoGain() {
		return infoGain;
	}
	public void setInfoGain(Double infoGain) {
		this.infoGain = infoGain;
	}
	public int getNumber() {
		return number;
	}
	public void setNumber(int number) {
		this.number = number;
	}
	public String getMajorityValue() {
		return majorityValue;
	}
	public void setMajorityValue(String majorityValue) {
		this.majorityValue = majorityValue;
	}


}
