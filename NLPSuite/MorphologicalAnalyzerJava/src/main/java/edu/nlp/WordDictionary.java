package edu.nlp;

public class WordDictionary {
	
	protected String word;
	protected String posTag;
	protected String root;
	
	public String getRoot() {
		return root;
	}
	public void setRoot(String root) {
		this.root = root;
	}
	public String getPosTag() {
		return posTag;
	}
	public void setPosTag(String posTag) {
		this.posTag = posTag;
	}
	public String getWord() {
		return word;
	}
	public void setWord(String word) {
		this.word = word;
	}
	
	@Override
	public String toString() {
		return word + " " + posTag + " ROOT " + root;
	}
	
}
