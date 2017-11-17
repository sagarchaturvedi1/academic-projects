package edu.nlp.next;

import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Map.Entry;
import java.util.Set;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/**
 * @author sagar 
 * Morphological Analyzer
 */
public class MorphologicalAnalyzer {
	public static List<WordDictionary> dictionaryList = new ArrayList<>();
	public static List<Rules> ruleList = new ArrayList<>();
	public static List<String> test = new ArrayList<>();
	public static int morphology = 0;
	public static int wordFound = 0;
	public static Map<String,Map<String,String>> branch = new LinkedHashMap<>();
	public static List<String> output = new ArrayList<>();
	
	@SuppressWarnings("unchecked")
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
			/*//System.out.println(dictionaryList + "\n\n\n");
*/			fillRulesList(rules);
			
			for (String string : test) {
				morphology = 0;
				wordFound = 0;
				branch.clear();
				searchDictionary(string, string);
				if(wordFound == 0) {
			        System.out.println(string + " noun" + " ROOT=" +string + " SOURCE=default");
				}
				System.out.println("\n");
			}
			

		} catch (Exception e) {
			e.printStackTrace();
		}

	}
	
	@SuppressWarnings("unchecked")
	private static int searchDictionary(String word, String word1) {
		int found = 0;
		for (WordDictionary wordDictionary : dictionaryList) {
			if (wordDictionary.getWord().equalsIgnoreCase(word)) {
				/*//System.out.println("Inside dictionary -------------------------------------");
*/				String posTag = wordDictionary.getPosTag();
				String root;
				if (wordDictionary.getRoot() == null) {
					root = "ROOT="+word;
				} else {
					root = "ROOT="+wordDictionary.getRoot();
				}
				Map<String,Map<String,String>> backupBranch = new LinkedHashMap<>(branch);
				printList(word1, posTag, root);
				found = 1;
				
				List<WordDictionary> listNextWords = new ArrayList<>(dictionaryList).stream().
						filter(line -> line.getWord().startsWith(word) && line.getNumber() == 0).collect(Collectors.toList());
				/*//System.out.println(" \n \n \n list of next words ----------- " + listNextWords + "\n\n\n");
*/				for (WordDictionary wordDic : listNextWords) {
					branch =  new LinkedHashMap<>(backupBranch);
					posTag = wordDic.getPosTag();
					if (wordDic.getRoot() == null) {
						root = "ROOT="+word;
					} else {
						root = "ROOT="+wordDic.getRoot();
					}
					/*//System.out.println("Found in dictionary inside next occurence loop ---------"+ word +","+ posTag);
*/					printList(word1, posTag, root);
				}
			} 
		}
		if(found==0) {
				traverse(word,word1);
		}
		return found;
		
	}
	
	@SuppressWarnings("unchecked")
	private static void traverse (String word, String word1) {
	    morphology = 1;
	    String newWord = null;
	   /* if(word.equals("previewer")) {
	    	System.out.println("stores is here");
	    }*/
	    for (Rules rule : ruleList) {
	    		    	
	    	if (rule.getAffixType().equalsIgnoreCase("SUFFIX")) {
				newWord = word.replaceAll(rule.getAffixWord()+"$",rule.getReplacementChar());
			} else {
				newWord = word.replaceFirst(rule.getAffixWord(), rule.getReplacementChar());
			}
	    	
	    	if(newWord != null && !word.equalsIgnoreCase(newWord)) {
	    		/*System.out.println(word + " " + rule.getAffixType() + " "  + rule.getAffixWord() + " "  + 
		    			rule.getReplacementChar() + " "  + rule.getPosAfter() + " "  + rule.getPosBefore());
*/	    		Map<String,String> posMap = new HashMap<>();
	    		
	    		posMap.put(rule.getPosAfter(), rule.getPosBefore());
	    		/*System.out.println("\n\n adding path to branch --------------------------"
	    				+ "--------------------" + posMap);*/
	    		branch.put(newWord, posMap);
	    		
	    		if(searchDictionary(newWord, word1)==0) {
	    			if(!branch.isEmpty()) {
	    				extractLastPath();
	    			}
	    		}
	    	}
	    	
		}
	    
	}
	
	@SuppressWarnings("unchecked")
	private static void printList(String word, String pos, String root) {
		/*//System.out.println("Dictionary returned with word and PoS ------ " + word + "," + pos + "\n\n");
*/		int valid = 1;
		String source = null;
		if(morphology == 1 && !branch.isEmpty()) {
	    	/*//System.out.println("branch ------ " + branch);
*/		    Entry<String, Map<String,String>> entry2 = extractLastPath();
		    String pos1 = getValueFromEntry(entry2,1);
		    valid = (pos.equalsIgnoreCase(pos1)) ?1 :0;
		    Iterator<Entry<String, Map<String,String>>> it = branch.entrySet().iterator();
		    while(!branch.isEmpty()) {
		    	/*//System.out.println("branch ------ " + branch);
*/		    	
		    	Entry<String, Map<String,String>> entry1 = extractLastPath();
			    /*//System.out.println("entry 2 --- " + entry2 + " ,entry1 ---- " + entry1);
			    //System.out.println("Entry 2 [2] compared with entry1[1] -------- " + getValueFromEntry(entry2,2).equalsIgnoreCase(getValueFromEntry(entry1,1)));
*/			    if(!getValueFromEntry(entry2,2).equalsIgnoreCase(getValueFromEntry(entry1,1))) {
			    		valid = 0;
			    }
			    entry2 = entry1;
		    }
		    pos = getValueFromEntry(entry2,2);
			source= "SOURCE=morphology";
		} else {
			source = "SOURCE=dictionary";
		}
		String outputString = word + " " + pos + " "+root + " " + source;
		if(!output.contains(outputString) && valid == 1) {
			System.out.println(outputString);
			output.add(outputString);
			wordFound = 1;
		}
	}

	@SuppressWarnings("unchecked")
	private static void fillDictionaryList(List<String> dictionary) {
		for (String line : dictionary) {
			line = line.trim();
			String[] words = line.split("\\s+");
			String word = words[0];
			
			for (WordDictionary wordDictionary : dictionaryList) {
				if(wordDictionary.getWord().equalsIgnoreCase(word)) {
					wordDictionary.setNumber(wordDictionary.getNumber()+1);
					word = word+wordDictionary.getNumber();
				}
			}
			
			WordDictionary searchDictionary = new WordDictionary();
			searchDictionary.setWord(word);
			searchDictionary.setPosTag(words[1].trim());
			if (words.length > 2 && words[2].trim().equalsIgnoreCase("root")) {
				searchDictionary.setRoot(words[3].trim());
			}
			dictionaryList.add(searchDictionary);
		}

	}

	@SuppressWarnings("unchecked")
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
		
	}
	
	@SuppressWarnings("unchecked")
	private static Entry<String, Map<String,String>> extractLastPath() {
		Entry<String, Map<String,String>> entry = null;
		if(!branch.isEmpty()) {
			final Set<Entry<String, Map<String,String>>> mapValues = branch.entrySet();
		    final int maplength = mapValues.size();
		    final Entry<String, Map<String,String>>[] test = new Entry[maplength];
		    mapValues.toArray(test);
		    entry = test[maplength-1];
			branch.remove(entry.getKey());
		}
		return entry;
	}
	
	@SuppressWarnings("unchecked")
	private static String getValueFromEntry(Entry<String, Map<String,String>> entry,int number) {
		String pos = "";
		if(entry != null) {
			if(number == 1) {
				pos = entry.getValue().keySet().iterator().next();
			} else if(number == 2) {
				pos = entry.getValue().values().iterator().next();
			}
		}
		return pos;
	}

}
