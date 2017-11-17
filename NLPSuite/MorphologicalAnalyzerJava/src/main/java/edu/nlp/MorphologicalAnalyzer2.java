package edu.nlp;

import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/**
 * @author sagar Morphological Analyzer
 */
public class MorphologicalAnalyzer2 {
	public static List<WordDictionary> dictionaryList = new ArrayList<>();
	public static List<Rules> ruleList = new ArrayList<>();
	public static List<String> test = new ArrayList<>();
	public static Set<Rules> doneRules = new HashSet<>();
	public static String searchWord = "";
	public static String initialPos = "";

	public static void main(String[] args) {
		if (args == null || args.length != 3) {
			System.out.println("ERROR IN INPUT! Please provide all the required input files.");
			System.out.println(
					"This morphological analyzer needs 3 input text files - Dictionary file, Rule file, Test File");
			System.out.println("... Exiting");
			System.exit(1);
		}

		String dictFile = args[0].trim();
		String ruleFile = args[1].trim();
		String testFile = args[2].trim();

		try (Stream<String> dictStream = Files.lines(Paths.get(dictFile));
				Stream<String> ruleStream = Files.lines(Paths.get(ruleFile));
				Stream<String> testStream = Files.lines(Paths.get(testFile))) {

			List<String> dictionary = dictStream.map(String::toLowerCase).collect(Collectors.toList());
			List<String> rules = ruleStream.map(line -> line.replaceAll("->", " ")).map(String::toLowerCase)
					.collect(Collectors.toList());
			test = testStream.map(String::toLowerCase).collect(Collectors.toList());

			if (dictionary.size() == 0) {
				System.out.println("ERROR IN INPUT! Dictionary file is empty.... Exiting");
				System.exit(1);
			}
			if (rules.size() == 0) {
				System.out.println("ERROR IN INPUT! Rules file is empty.... Exiting");
				System.exit(1);
			}
			if (test.size() == 0) {
				System.out.println("ERROR IN INPUT! Test file is empty.... Exiting");
				System.exit(1);
			}

			fillDictionaryList(dictionary);
			fillRulesList(rules);
			//Set<String> finalResults = new HashSet<>();
			
			for (String string : test) {
				searchWord = string;
				List<Rules> listOfRules = new ArrayList<>(ruleList);
				Set<String> results = new HashSet<>();
				results = search(string,listOfRules,results);
				if(results.isEmpty()) {
					Output output = new Output();
					output.setWord(string);
					output.setPosTag("noun");
					output.setRoot(string);
					output.setSource("default");
					results.add(output.toString());
				}
				
				for (String result : results) {
					System.out.println(result);
				}
				System.out.println("\n");
				searchWord = "";
			}
			/*for (String result : finalResults) {
				System.out.println(result);
			}*/

		} catch (Exception e) {
			e.printStackTrace();
		}

	}

	private static void fillDictionaryList(List<String> dictionary) {
		for (String line : dictionary) {
			line = line.trim();
			String[] words = line.split("\\s+");
			WordDictionary searchDictionary = new WordDictionary();
			searchDictionary.setWord(words[0].trim());
			searchDictionary.setPosTag(words[1].trim());
			if (words.length > 2 && words[2].trim().equalsIgnoreCase("ROOT")) {
				searchDictionary.setRoot(words[3].trim());
			}
			dictionaryList.add(searchDictionary);
		}

	}

	private static void fillRulesList(List<String> rules) {
		for (String line : rules) {
			line = line.trim();
			String[] words = line.split("\\s+");
			Rules ruleObject = new Rules();
			ruleObject.setAffixType(words[0]);
			ruleObject.setAffixWord(words[1]);
			if (words[2].trim().equals("-")) {
				ruleObject.setReplacementChar("");
			} else {
				ruleObject.setReplacementChar(words[2]);
			}
			ruleObject.setPosAfter(words[3]);
			ruleObject.setPosBefore(words[4]);
			ruleList.add(ruleObject);
		}
		
		/*for (Rules rule : ruleList) {
			List<Rules> childRules = new ArrayList<>(ruleList);
			childRules.remove(rule);
			rule.setChildRules(childRules);
		}*/
	}

	private static Map<String, String> applyRule(String word, Rules rule) {
		Map<String, String> result = new HashMap<>();
		if (rule.getAffixType().equalsIgnoreCase("SUFFIX")) {
			int lastIndex = word.lastIndexOf(rule.getAffixWord());
			if(lastIndex != -1) {
				word = word.substring(0, lastIndex) + rule.getReplacementChar();
			}
			/*word = new StringBuilder(word).reverse().toString().
					replaceFirst(rule.getAffixWord(), rule.getReplacementChar());
			word = new StringBuilder(word).reverse().toString();*/
		} else {
			word = word.replaceFirst(rule.getAffixWord(), rule.getReplacementChar());
		}
		result.put(word, rule.getPosAfter());
		return result;
	}

	private static Output searchDictionary(String word, String source) {
		Output result = null;
		for (WordDictionary wordDictionary : dictionaryList) {
			if (wordDictionary.getWord().equalsIgnoreCase(word)) {
				result = new Output();
				result.setPosTag(wordDictionary.getPosTag());
				result.setWord(wordDictionary.getWord());
				result.setSource(source);
				if (wordDictionary.getRoot() == null) {
					result.setRoot(word);
				} else {
					result.setRoot(wordDictionary.getRoot());
				}
				break;
			}
		}
		return result;
	}

	private static Set<String> search(String word, List<Rules> rules, Set<String> results) {
		Output output = searchDictionary(word,"dictionary");
		if (output != null && test.contains(word)) {
			results.add(output.toString());
		} else {
			results.addAll(traverse(word, rules, results, ""));
			/*for(int i=0;i<rules.size();i++) {
				Rules rule = rules.get(i);
				Map<String,String> ruleResult = applyRule(word, rule);
				String word1 = ruleResult.keySet().iterator().next();
				String posTag = ruleResult.get(word1);
				Output output1 = searchDictionary(word);
				if (output1 != null && output1.getPosTag().equalsIgnoreCase(posTag)) {
					output1.setSource("morphology");
					results.add(output1.toString());
				} else {
					List<Rules> remainingRules = new ArrayList<>(rules);
					remainingRules.remove(rule);
					search(word1, remainingRules, results, "morphology");
				}
				
				
			}*/
			
			/*Iterator<Rules> it = rules.iterator();
			while(it.hasNext()) {
				Rules rule = it.next();
				//System.out.println("Current rule - "+rule.toString()+" || Parent rule -" +parentRule);

				if(rule.toString().equalsIgnoreCase(parentRule)) {
					break;
				}
				Map<String,String> ruleResult = applyRule(word, rule);
				String word1 = ruleResult.keySet().iterator().next();
				String posTag1 = ruleResult.get(word1);
				Output output1 = searchDictionary(word,source);
				if (output1 != null && output1.getPosTag().equalsIgnoreCase(posTag1)) {
					output1.setSource("morphology");
					results.add(output1.toString());
				} else {
					List<Rules> nextPossibleRules = getNextPossibleRules(rule, rule.getChildRules());
					search(word1,nextPossibleRules,results,"morphology",rule.toString());
				}
				//System.out.println("\n");
			}*/
		}
		
		return results;
	}
	
	private static Set<String> traverse(String word, List<Rules> rules, Set<String> results, String posTag) {
		for (int i = 0; i < rules.size(); i++) {
			Rules rule = rules.get(i);
			
			Map<String, String> ruleResult = applyRule(word, rule);
			String word1 = ruleResult.keySet().iterator().next();
			String posTag1 = ruleResult.get(word1);
			//System.out.println(ruleResult);
			Output output1 = searchDictionary(word1,"morphology");
			if (output1 != null && output1.getPosTag().equalsIgnoreCase(posTag1)) {
				if(word.equalsIgnoreCase(searchWord)) {
					output1.setSource("morphology");
					output1.setWord(word);
					output1.setPosTag(rule.getPosBefore());
					results.add(output1.toString());
				} else {
					output1.setSource("morphology");
					output1.setWord(searchWord);
					output1.setPosTag(posTag);
					results.add(output1.toString());
					/*List<Rules> nextRules = getNextPossibleRules(posTag, new ArrayList<Rules>(ruleList),true);
					traverse(word, nextRules, results,posTag);	
					internalDoneRules.add(rule);*/
				}
				//internalDoneRules.clear();
			} 			
			/*List<Rules> remainingRules = new ArrayList<>(rules);
			remainingRules.remove(rule);*/
			doneRules.add(rule);
			List<Rules> remainingRules = getNextPossibleRules(rule, rules);
			traverse(word1, remainingRules, results,posTag1);			
		}
		doneRules.clear();
		return results;
	}

	/*private static Integer getOutputKey(Output output) {
		StringBuilder sb = new StringBuilder();
		sb.append(output.getWord()).append(output.getPosTag()).append(output.getRoot()).append(output.getSource());

		return sb.toString().hashCode();

	}*/

	private static List<Rules> getNextPossibleRules(Rules rule1,List<Rules> rules) {
		List<Rules> possibleRules = rules.stream().filter(rule -> rule.getPosBefore().equalsIgnoreCase(rule1.getPosAfter()))
				//.filter(rule -> !doneRules.contains(rule))
				.collect(Collectors.toList());
		Iterator<Rules> it = possibleRules.iterator();
		while(it.hasNext()) {
			String ruleString = it.next().toString();
			for (Rules rules2 : doneRules) {
				if(rules2.toString().equalsIgnoreCase(ruleString)) {
					it.remove();
				}
			}
		}
		/*System.out.println("Rule is --- " + rule1);
		System.out.println("Possible Rule is --- " + possibleRules);
		System.out.println("Done Rule are ---- " + doneRules);
		System.out.println("\n");
		System.out.println("\n");*/
		return possibleRules;
	}
	
	/*private static List<Rules> getNextPossibleRules(String posTag,List<Rules> rules,boolean flag) {
		List<Rules> possibleRules = rules.stream().filter(rule -> rule.getPosBefore().equalsIgnoreCase(posTag))
				//.filter(rule -> !doneRules.contains(rule))
				.collect(Collectors.toList());
		Iterator<Rules> it = possibleRules.iterator();
		while(it.hasNext()) {
			String ruleString = it.next().toString();
			for (Rules rules2 : internalDoneRules) {
				if(rules2.toString().equalsIgnoreCase(ruleString)) {
					it.remove();
				}
			}
		}
		System.out.println("Rule is --- " + rule1);
		System.out.println("Possible Rule is --- " + possibleRules);
		System.out.println("Done Rule are ---- " + doneRules);
		System.out.println("\n");
		System.out.println("\n");
		return possibleRules;
	}*/

}
