package edu.decisionTree;

import java.io.IOException;
import java.io.Serializable;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;
import java.util.stream.Stream;

public class SampleData implements Serializable {
	
	/**
	 * 
	 */
	private static final long serialVersionUID = 1L;

	public static final String SEPARATOR = ",";

	private List<List<String>> data;
				
	public void setData(List<List<String>> data) {
		this.data = data;
	}

	public List<List<String>> getData() {
		return data;
	}
	
	public SampleData() {
		super();
	}
	
	public SampleData(String fileName) {
		data = new ArrayList<>();
		try(Stream<String> stream = Files.lines(Paths.get(fileName));) {
			if (Files.lines(Paths.get(fileName)).count() == 0) {
				System.out.println("ERROR IN INPUT! File " + fileName + " is empty.... Exiting");
				System.exit(1);
			}
			List<List<String>> fileData = stream.map(String::toLowerCase).map(line -> Arrays.asList(line.split(","))).collect(Collectors.toList());
			data.addAll(fileData);
		} catch (IOException e) {
			e.printStackTrace();
		}
	} 

	public SampleData(List<String> fileNames) {
		data = new ArrayList<>();
		for (String fileName : fileNames) {
			try(Stream<String> stream = Files.lines(Paths.get(fileName));) {
				if (Files.lines(Paths.get(fileName)).count() == 0) {
					System.out.println("ERROR IN INPUT! File " + fileName + " is empty.... Exiting");
					System.exit(1);
				}
				List<List<String>> fileData = stream.map(String::toLowerCase).map(line -> Arrays.asList(line.split(","))).collect(Collectors.toList());
				data.addAll(fileData);
			} catch (IOException e) {
				e.printStackTrace();
			}
		}
	}
	
	public Map<String,Long> getLabels() {
		Map<String,Long> classes = new HashMap<String, Long>();
		for (List<String> list : data) {
			String className = list.get(list.size()-1);
			long count = 1;
			if(classes.containsKey(className)) {
				count += classes.get(className);
			}
			classes.put(className, count);
		}
		return classes;
	}
	
	public static Map<String,Long> getLabels(List<List<String>> dataList) {
		Map<String,Long> classes = new HashMap<String, Long>();
		for (List<String> list : dataList) {
			String className = list.get(list.size()-1);
			long count = 1;
			if(classes.containsKey(className)) {
				count += classes.get(className);
			}
			classes.put(className, count);
		}
		return classes;
	}
	
	public static String getMaxLabel(List<List<String>> dataList) {
		Map<String,Long> classes = new HashMap<String, Long>();
		for (List<String> list : dataList) {
			String className = list.get(list.size()-1);
			long count = 1;
			if(classes.containsKey(className)) {
				count += classes.get(className);
			}
			classes.put(className, count);
		}
		
		long maxCount = 0;
		String maxLabel = "";
		for (String label : classes.keySet()) {
			Long count = classes.get(label);
			if(count > maxCount) {
				maxCount = count;
				maxLabel = label;
			}
		}
		
		return maxLabel;
	}

	
}
