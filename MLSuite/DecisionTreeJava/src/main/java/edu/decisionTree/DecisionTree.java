package edu.decisionTree;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Map.Entry;
import java.util.Set;
import java.util.stream.Collectors;

public class DecisionTree implements Serializable {

	/**
	 * 
	 */
	private static final long serialVersionUID = 1L;

	private int maxDepth;
	private String parentValue;

	private List<DecisionTree> childNodes = new ArrayList<>();

	private Attribute attribute;

	private SampleData sampleData;

	private String label;

	private boolean isLeaf = false;

	public DecisionTree(int maxDepth, String parentValue) {
		this.setParentValue(parentValue);
		this.maxDepth = maxDepth;
	}

	public DecisionTree createDecisionTree(List<Attribute> attributes, SampleData sd, int currentDepth) {
		
		this.sampleData = sd;
		List<List<String>> data = this.sampleData.getData();
		
		if (data == null || data.size() == 0 || attributes == null || attributes.size() == 0) {
			return this;
		} else {
			Map<String, Long> labels = sampleData.getLabels();
			if(currentDepth >= maxDepth && maxDepth != -1) {
				this.label = getMaxCountLabel(labels).getKey();
				this.isLeaf = true;
			} else {
				if (labels.size() == 1) {
					this.label = labels.keySet().iterator().next();
					this.isLeaf = true;
				} else {
					// currentDepth++;
					attribute = getBestAttribute(attributes, labels);
					/*
					 * System.out.println("Attribute - " +
					 * attribute.getName() + ", Info gain - " +
					 * attribute.getInfoGain());
					 */
					Map<String, SampleData> dividedData = divideData(attribute);
					List<Attribute> newAttributes = attributes.stream()
							.filter(line -> !line.getName().equalsIgnoreCase(attribute.getName()))
							.collect(Collectors.toList());
					for (String value : dividedData.keySet()) {
						DecisionTree decisionTree = new DecisionTree(maxDepth, value);
						SampleData valueData = dividedData.get(value);
						childNodes.add(decisionTree.createDecisionTree(newAttributes, valueData,
								currentDepth + 1));
					}

				}
			}
			
			}
			
		return this;
	}

	private double getEntropy(Map<String, Long> labels) {
		double totalRecords = labels.values().stream()
				.collect(Collectors.summingLong(line -> line));
		double entropy = 0;
		for (double value : labels.values()) {
			/*
			 * System.out.println((value / totalRecords));
			 * System.out.println((Math.log10(value /
			 * totalRecords) / Math.log10(2)));
			 */
			entropy = (value == 0) ? 0
					: entropy - (value / totalRecords)
							* (Math.log10(value / totalRecords) / Math.log10(2));
		}
		return entropy;

	}

	private double getEntropy(Attribute attribute, Set<String> labels) {
		double entropy = 0.0;
		double totalDataSize = sampleData.getData().size();
		for (String value : attribute.getValues()) {
			final int attIndex = attribute.getNumber();
			double fieldEntropy = 0.0;
			List<List<String>> data = new ArrayList<>(sampleData.getData());
			List<List<String>> dataForAttr = data.stream()
					.filter(line -> line.get(attIndex).equalsIgnoreCase(value))
					.collect(Collectors.toList());
			double valueCount = dataForAttr.size();
			if (valueCount != 0) {
				for (String label : labels) {
					List<List<String>> list = new ArrayList<>(dataForAttr);
					int size = list.get(0).size();
					double labelCount = list.stream()
							.filter(line -> line.get(size - 1).equalsIgnoreCase(label)).count();
					fieldEntropy = (labelCount == 0) ? 0
							: (fieldEntropy - (labelCount / valueCount)
									* (Math.log10(labelCount / valueCount) / Math.log10(2)));
					// fieldEntropy -=
					// (labelCount/totalDataSize)*(Math.log10(labelCount/totalDataSize)/Math.log10(2));
					list.clear();
				}
				fieldEntropy *= (valueCount / totalDataSize);
			}
			entropy += fieldEntropy;
			data.clear();
			dataForAttr.clear();
		}
		return entropy;
	}

	private double getInfoGain(Attribute attribute, double totalEntropy, Set<String> labels) {
		double entropy = getEntropy(attribute, labels);
		return totalEntropy - entropy;
	}

	private Attribute getBestAttribute(List<Attribute> attributes, Map<String, Long> labels) {
		double totalEntropy = getEntropy(labels);
		for (Attribute attribute : attributes) {
			attribute.setInfoGain(getInfoGain(attribute, totalEntropy, labels.keySet()));
		}
		Collections.sort(attributes, Collections.reverseOrder(new AttributeComparator()));
		return attributes.get(0);
	}

	private Map<String, SampleData> divideData(Attribute attribute) {
		Map<String, SampleData> dividedData = new HashMap<>();
		for (String value : attribute.getValues()) {
			SampleData sd = new SampleData();
			List<List<String>> data = new ArrayList<>(sampleData.getData());
			final int cnt = attribute.getNumber();
			List<List<String>> dataForAttr = data.stream()
					.filter(line -> line.get(cnt).equalsIgnoreCase(value))
					.collect(Collectors.toList());
			sd.setData(dataForAttr);
			dividedData.put(value, sd);
		}
		return dividedData;
	}

	public String print() {
		String tree = "maxDepth = " + maxDepth + "\n";
		if (isLeaf) {
			tree = tree + " This is a leaf node. \n";
		}

		if (parentValue != null) {
			tree = tree + "edge value = " + parentValue + "\n";
		} else {
			tree = tree + " This is the root node. \n";
		}

		if (attribute != null) {
			tree = tree + "attribute = " + attribute.getName() + "\n" + "attribute info gain = "
					+ attribute.getInfoGain() + "\n";
		}

		if (sampleData != null && sampleData.getData() != null) {
			tree = tree + "data size = " + sampleData.getData().size() + "\n";
		}
		if (label != null) {
			tree = tree + "label = " + label + "\n";
		}

		tree = tree + "\tChildren = \n\t";
		for (DecisionTree decisionTree : childNodes) {
			tree = tree + decisionTree.print();
		}
		return tree;

		/*
		 * try { FileOutputStream fileOut = new
		 * FileOutputStream("decisionTree.ser");
		 * ObjectOutputStream out = new
		 * ObjectOutputStream(fileOut);
		 * out.writeObject(this); out.close();
		 * fileOut.close(); System.out.
		 * printf("Serialized data is saved in decisionTree.ser"
		 * ); } catch (Exception e) { e.printStackTrace(); }
		 */
	}

	public String getParentValue() {
		return parentValue;
	}

	public void setParentValue(String parentValue) {
		this.parentValue = parentValue;
	}

	public boolean isLeaf() {
		return isLeaf;
	}

	public void setLeaf(boolean isLeaf) {
		this.isLeaf = isLeaf;
	}

	/*public List<List<String>> predictClass(List<List<String>> testData, List<List<String>> output) {
		if (testData != null && !testData.isEmpty()) {
			if (isLeaf) {
				for (List<String> list : testData) {
					list.set(list.size() - 1, this.label);
					output.add(list);
				}
				
				 * output.add(testData.stream().map(line ->
				 * line.set(line.size() - 1, this.label))
				 * .collect(Collectors.toList()));
				 
			} else {
				final int attributeNumber = attribute.getNumber();
				for (DecisionTree childNode : childNodes) {
					List<List<String>> data = new ArrayList<>(testData);
					List<List<String>> nodeData = data.stream()
							.filter(line -> line.get(attributeNumber)
									.equalsIgnoreCase(childNode.parentValue))
							.collect(Collectors.toList());
					childNode.predictClass(nodeData, output);
				}
			}
		}

		return output;
	}*/
	
	public String predictClass(List<String> row) {
		String label = "";
		if(isLeaf) {
			label = this.label;
		} else {
			for (DecisionTree tree : childNodes) {
				String value = row.get(this.attribute.getNumber());
				if(value != null && value.toLowerCase().equalsIgnoreCase(tree.parentValue)) {
					label = tree.predictClass(row);
					break;
				}
			}
		}
		return label;
	}

	public int getDepth() {
		int i = 0;
		if (!this.childNodes.isEmpty()) {
			i++;
			List<Integer> depths = new ArrayList<>();
			for (DecisionTree decisionTree : childNodes) {
				depths.add(decisionTree.getDepth());
			}
			Collections.sort(depths, Collections.reverseOrder());
			i = i + depths.get(0);
		}
		return i;
	}

	private static Entry<String, Long> getMaxCountLabel(Map<String, Long> labels) {
		Entry<String, Long> maxEntry = null;
		for (Entry<String, Long> entry : labels.entrySet()) {
			if (maxEntry == null || entry.getValue() > maxEntry.getValue()) {
				maxEntry = entry;
			}
		}
		return maxEntry;
	}

}