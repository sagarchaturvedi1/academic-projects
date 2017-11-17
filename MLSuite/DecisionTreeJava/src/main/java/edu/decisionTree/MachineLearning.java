package edu.decisionTree;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.stream.Collectors;
import java.util.stream.Stream;

public class MachineLearning {

	public static Set<Integer> depthSet = new HashSet<>(Arrays.asList(1,2,3,4,5,10,15,20));
	public static Map<Integer,String> treatmentSet = new HashMap<Integer,String>();
	public static Map<Integer,Map<String,String>> majorityLabelFeatureValue = new HashMap<>();
	
	static {
		treatmentSet.put(1, "Replace missing data with majority value of that feature");
		treatmentSet.put(2, "Replace missing data with majority value of that feature against that label");
		treatmentSet.put(3, "Don't replace missing data");
	}

	public void predict(String trainingFile, String testFile, int maxDepth, boolean treatMissing) {
		File file = new File(trainingFile);
		if(!file.exists() || file.isDirectory()) {
			System.out.println("ERROR IN INPUT! Given training file does not exist OR it is a directory\n");
			System.exit(1);
		}
		
		file = new File(testFile);
		if(!file.exists() || file.isDirectory()) {
			System.out.println("ERROR IN INPUT! Given test file does not exist OR it is a directory\n");
			System.exit(1);
		}
		
		SampleData trainingData = new SampleData(trainingFile);
		SampleData testData = new SampleData(testFile);
		List<Attribute> attributes = getAttributes(trainingData.getData());
		
		// If treat missing flag is on
		if(treatMissing) {
			int treatment = maxDepth;
			maxDepth = -1;
			if(treatment==1) {
				trainingData.setData(replaceMissingWithMajorityValue(trainingData.getData()));
				testData.setData(replaceMissingWithMajorityValue(testData.getData()));
			} else if(treatment==2) {
				trainingData.setData(replaceMissingWithMajorityLabelValue(trainingData.getData(),true));
				testData.setData(replaceMissingWithMajorityLabelValue(testData.getData(),false));
			}
		}
		
		DecisionTree decisionTree = new DecisionTree(maxDepth,null);
		decisionTree.createDecisionTree(attributes,trainingData,0);
		
		System.out.println("Depth of the tree is ------- " + decisionTree.getDepth());
		
		/*List<List<String>> output = new ArrayList<>();
		output = decisionTree.predictClass(testData.getData(),output);
		System.out.println(output.size());*/
		List<List<String>> output = new ArrayList<>(testData.getData());
		
		double localAccuracy = 0;
		String maxLabel = SampleData.getMaxLabel(trainingData.getData());
		for (List<String> row : output) {
			String label = decisionTree.predictClass(row);
			if(label == null || label.isEmpty()) {
				label = maxLabel;
			}
			if(row.get(row.size()-1).equalsIgnoreCase(label)) {
				localAccuracy++;
			}
		}		
		
		localAccuracy = 100*(localAccuracy/output.size());
		
		System.out.println("Test Accuracy ---" + localAccuracy);
		System.out.println("Test Error ---" + (100 - localAccuracy));
	}
	
	public void evaluate(String directoryName) {
		File file = new File(directoryName);
		if(!file.exists() || !file.isDirectory() || file.list().length == 0) {
			System.out.println("ERROR IN INPUT! Given cross validation data directory does not exist OR it is not a directory"
					+ " OR the directory is empty\n");
			System.exit(1);
		}
		
		double error = 0;
		
		List<File> cvFiles = Arrays.asList(file.listFiles());
		
		System.out.println("Total number of cross validation files - " + cvFiles.size());
		System.out.println("Starting " + cvFiles.size() + "-fold cross validation ------------ ");

		
		for (File cvFile : cvFiles) {
			List<File> dupFiles = new ArrayList<>(cvFiles);
			List<String> trainingFiles = new ArrayList<>(dupFiles.stream().map(line -> line.getAbsolutePath()).collect(Collectors.toList()));
			trainingFiles.remove(cvFile.getAbsolutePath());
			String testFileName = cvFile.getAbsolutePath();
			
			SampleData trainingData = new SampleData(trainingFiles);
			DecisionTree decisionTree = new DecisionTree(-1,null);
			decisionTree.createDecisionTree(getAttributes(trainingData.getData()),trainingData,0);
			
			SampleData testData = new SampleData(testFileName);
			/*List<List<String>> output = new ArrayList<>();
			output = decisionTree.predictClass(testData.getData(),output);*/
			
			List<List<String>> output = new ArrayList<>(testData.getData());
			double localAccuracy = 0;

			String maxLabel = SampleData.getMaxLabel(trainingData.getData());
			for (List<String> row : output) {
				/*row.set(row.size()-1, decisionTree.predictClass(row));*/
				String label = decisionTree.predictClass(row);
				if(label == null || label.isEmpty()) {
					label = maxLabel;
				}
				if(row.get(row.size()-1).equalsIgnoreCase(label)) {
					localAccuracy++;
				}
			}		
			
			localAccuracy = 100*(localAccuracy/output.size());
			double cycleError = 100-localAccuracy;
			error += cycleError;
			
			System.out.println("Cycle Error for training files " +  trainingFiles + " and test file " + testFileName
					+ " = " + cycleError);
		} 
		
		error /= cvFiles.size();
		System.out.println("Average CV error = " + error);
	}
	
	public void evaluateDepth(String directoryName) {
		File file = new File(directoryName);
		if(!file.exists() || !file.isDirectory() || file.list().length == 0) {
			System.out.println("ERROR IN INPUT! Given cross validation data directory does not exist OR it is not a directory"
					+ " OR the directory is empty\n");
			System.exit(1);
		}
				
		List<File> cvFiles = Arrays.asList(file.listFiles());
		
		System.out.println("Total number of cross validation files - " + cvFiles.size());
		System.out.println("Starting " + cvFiles.size() + "-fold cross validation ------------ ");

		for (Integer depth : depthSet) {
			double accuracy = 0;
			double standardDev = 0;
			List<Double> list = new ArrayList<>();
			double size = cvFiles.size();
			
			for (File cvFile : cvFiles) {
				List<File> dupFiles = new ArrayList<>(cvFiles);
				List<String> trainingFiles = new ArrayList<>(dupFiles.stream().map(line -> line.getAbsolutePath()).collect(Collectors.toList()));
				trainingFiles.remove(cvFile.getAbsolutePath());
				String testFileName = cvFile.getAbsolutePath();
				
				SampleData trainingData = new SampleData(trainingFiles);
				DecisionTree decisionTree = new DecisionTree(depth,null);
				decisionTree.createDecisionTree(getAttributes(trainingData.getData()),trainingData,0);
				/*System.out.println("For depth "+ depth + ",Tree size = " + decisionTree.getDepth());*/

				SampleData testData = new SampleData(testFileName);
				/*List<List<String>> output = new ArrayList<>();
				output = decisionTree.predictClass(testData.getData(),output);*/
				
				List<List<String>> output = new ArrayList<>(testData.getData());
				double localAccuracy = 0;
				String maxLabel = SampleData.getMaxLabel(trainingData.getData());
				for (List<String> row : output) {
					/*row.set(row.size()-1, decisionTree.predictClass(row));*/
					String label = decisionTree.predictClass(row);
					if(label == null || label.isEmpty()) {
						label = maxLabel;
					}
					if(row.get(row.size()-1).equalsIgnoreCase(label)) {
						localAccuracy++;
					}
				}
				/*double localAccuracy = calculateStats(testData.getData(), output).get("accuracy");*/
				accuracy += (localAccuracy/output.size());
				list.add(localAccuracy/output.size()); 
				
			} 
			
			/*System.out.println(list);*/
			accuracy /= cvFiles.size(); 
			System.out.println("For depth "+ depth + ",Average Cross validation accuracy = " + (accuracy*100));
			

			for (Double number : list) {
				double difference = (number - accuracy)*(number - accuracy);
				standardDev += difference;
			}
			
			standardDev *=100*100;
			standardDev /=size;
			System.out.println("For depth "+ depth + ",Cross validation standard deviation = " + Math.sqrt(standardDev) + "\n");
			
		}
		
	}
	
	public void evaluateMissing(String directoryName) {
		File file = new File(directoryName);
		if(!file.exists() || !file.isDirectory() || file.list().length == 0) {
			System.out.println("ERROR IN INPUT! Given cross validation data directory does not exist OR it is not a directory"
					+ " OR the directory is empty\n");
			System.exit(1);
		}
				
		List<File> cvFiles = Arrays.asList(file.listFiles());
		
		System.out.println("Total number of cross validation files - " + cvFiles.size());
		System.out.println("Starting " + cvFiles.size() + "-fold cross validation ------------ ");

		for (Integer treatment : treatmentSet.keySet()) {
			System.out.println("Starting CV for treatment \""+ treatmentSet.get(treatment) + "\"");
			double accuracy = 0;
			double standardDev = 0;
			List<Double> list = new ArrayList<>();
			double size = cvFiles.size();
			
			for (File cvFile : cvFiles) {
				List<File> dupFiles = new ArrayList<>(cvFiles);
				List<String> trainingFiles = new ArrayList<>(dupFiles.stream().map(line -> line.getAbsolutePath()).collect(Collectors.toList()));
				trainingFiles.remove(cvFile.getAbsolutePath());
				String testFileName = cvFile.getAbsolutePath();
				
				SampleData trainingData = new SampleData(trainingFiles);
				SampleData testData = new SampleData(testFileName);
				
				
				if(treatment==1) {
					trainingData.setData(replaceMissingWithMajorityValue(trainingData.getData()));
					testData.setData(replaceMissingWithMajorityValue(testData.getData()));
				} else if(treatment==2) {
					trainingData.setData(replaceMissingWithMajorityLabelValue(trainingData.getData(),true));
					testData.setData(replaceMissingWithMajorityLabelValue(testData.getData(),false));
				}
								
				DecisionTree decisionTree = new DecisionTree(-1,null);
				decisionTree.createDecisionTree(getAttributes(trainingData.getData()),trainingData,0);
				/*System.out.println("For treatment \""+ treatmentSet.get(treatment) + "\" tree depth is --- " + decisionTree.getDepth());*/

				/*List<List<String>> output = new ArrayList<>();
				output = decisionTree.predictClass(testData.getData(),output);*/
				
				List<List<String>> output = new ArrayList<>(testData.getData());
				double localAccuracy = 0;
				String maxLabel = SampleData.getMaxLabel(trainingData.getData());
				for (List<String> row : output) {
					/*row.set(row.size()-1, decisionTree.predictClass(row));*/
					String label = decisionTree.predictClass(row);
					if(label == null || label.isEmpty()) {
						label = maxLabel;
					}
					if(row.get(row.size()-1).equalsIgnoreCase(label)) {
						localAccuracy++;
					}
				}
				/*double localAccuracy = calculateStats(testData.getData(), output).get("accuracy");*/
				accuracy += (localAccuracy/output.size());
				list.add(localAccuracy/output.size()); 
				
			} 
			
			/*System.out.println(list);*/
			accuracy /= cvFiles.size(); 
			System.out.println("For treatment \""+ treatmentSet.get(treatment) + "\",Average Cross validation accuracy = " + (accuracy*100));
			

			for (Double number : list) {
				double difference = (number - accuracy)*(number - accuracy);
				standardDev += difference;
			}
			
			standardDev *=100*100;
			standardDev /=size;
			System.out.println("For treatment \""+ treatmentSet.get(treatment) + "\",Cross validation standard deviation = " + Math.sqrt(standardDev) + "\n");
			majorityLabelFeatureValue.clear();
		}
		
	}
	
	/*private Map<String,Double> calculateStats(List<List<String>> input, List<List<String>> output) {
		Map<String,Long> inputClasses = SampleData.getLabels(input);
		Map<String,Long> outputClasses = SampleData.getLabels(output);
		
		double error = 0;
		double accuracy = 0;
		double incorrectClassification = 0;
		double size = input.size();
		for (String targetClass : inputClasses.keySet()) {
			double inputCount = inputClasses.get(targetClass);
			double outputCount = outputClasses.get(targetClass);
			incorrectClassification += inputCount - outputCount;
		}
		
		error = 100*incorrectClassification/size;
		accuracy = 100 - error;
		
		Map<String, Double> matrix = new HashMap<>();
		matrix.put("error", error);
		matrix.put("accuracy", accuracy);
		return matrix;

	}*/
	
	
	private static List<Attribute> getAttributes(List<List<String>> data) {
		List<Attribute> attributes = new ArrayList<>();
		if(data.size() != 0) {
			Stream<String> stream;
			try {
				stream = Files.lines(Paths.get("FeatureNames"));
				int count = 0;
				Iterator<String> it = stream.iterator();
				while(it.hasNext()) {
					final int cnt = count;
					String featureName = it.next().trim().toLowerCase();
					Attribute attribute = new Attribute();
					attribute.setName(featureName);
					Set<String> values = data.stream().map(line -> line.get(cnt)).collect(Collectors.toSet());
					attribute.setValues(values);
					attribute.setNumber(cnt);
					attributes.add(attribute);
					count++;
				}
			} catch (IOException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		}		
		return attributes;
	}
	
	public static List<List<String>> replaceMissingWithMajorityValue(List<List<String>> data) {
		List<Attribute> attributes = getAttributes(data);
		for (Attribute attribute : attributes) {
			String majorityValue="";
			int maxCount=0;
			for (String value : attribute.getValues()) {
				if(value.equalsIgnoreCase("?")) {
					continue;
				}
				int count = data.stream().filter(line -> line.get(attribute.getNumber()).equalsIgnoreCase(value)).collect(Collectors.toList()).size();
				if(count >= maxCount) {
					maxCount = count;
					majorityValue = value;
				}
			}
			final String featureValue = majorityValue;
			data = data.stream().map(line -> {if((line.get(attribute.getNumber())).equalsIgnoreCase("?"))line.
				set(attribute.getNumber(), featureValue); return line;}).collect(Collectors.toList());
		}
		return data;
	}
	
	public static List<List<String>> replaceMissingWithMajorityLabelValue(List<List<String>> data,boolean training) {
		List<Attribute> attributes = getAttributes(data);
		Map<String,Long> labels = SampleData.getLabels(data);
		
		for (Attribute attribute : attributes) {
			if(training) {
				Map<String,String> labelMajorityValueMap = new HashMap<>();
				for (String label : labels.keySet()) {
					int maxCount=0;
					for (String value : attribute.getValues()) {
					if(value.equalsIgnoreCase("?")) {
						continue;
					}
					int count = data.stream().filter(line -> line.get(line.size()-1).equalsIgnoreCase(label))
							.filter(line -> line.get(attribute.getNumber()).equalsIgnoreCase(value))
							.collect(Collectors.toList()).size();
					if(count >= maxCount) {
						maxCount = count;
						labelMajorityValueMap.put(label, value);
					}
					
					}
				}
				
				majorityLabelFeatureValue.put(attribute.getNumber(), labelMajorityValueMap);
				data = data.stream().map(line -> {if((line.get(attribute.getNumber())).equalsIgnoreCase("?"))line.
					set(attribute.getNumber(), labelMajorityValueMap.get(line.get(line.size()-1))); return line;}).collect(Collectors.toList());
			} else {
				data = data.stream().map(line -> {if((line.get(attribute.getNumber())).equalsIgnoreCase("?"))line.
					set(attribute.getNumber(), majorityLabelFeatureValue.get(attribute.getNumber()).get(line.get(line.size()-1))); return line;})
						.collect(Collectors.toList());
				
			}
			
			/*System.out.println("feature Name - " + attribute.getName());
			System.out.println("Majority values - " + labelMajorityValueMap);*/

			
		}
		return data;
	}

}
