package edu.nlp.next;

public class WordDictionary {
	
	protected String word;
	protected String posTag;
	protected String root;
	private int number = 0;
	
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
		return word + " " + posTag + " ROOT " + root + " Number="+number;
	}
	public int getNumber() {
		return number;
	}
	public void setNumber(int number) {
		this.number = number;
	}
	
}
