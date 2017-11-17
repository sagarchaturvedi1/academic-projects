package edu.decisionTree;

import java.util.Comparator;

public class AttributeComparator implements Comparator<Attribute> {

	@Override
	public int compare(Attribute o1, Attribute o2) {
		Attribute attribute1 = (Attribute) o1;
		Attribute attribute2 = (Attribute) o2;
		return (attribute1.getInfoGain() >= attribute2.getInfoGain())?1:-1;
		//return attribute1.getInfoGain().compareTo(attribute2.getInfoGain());
	}

}
