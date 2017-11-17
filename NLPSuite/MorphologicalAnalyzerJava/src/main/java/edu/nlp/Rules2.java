package edu.nlp;

public class Rules2 {

	private String affixType;
	private String affixWord;
	private String replacementChar;
	private String posBefore;
	private String posAfter;
	//private List<Rules> childRules;
	
	public String getAffixType() {
		return affixType;
	}
	public void setAffixType(String affixType) {
		this.affixType = affixType;
	}
	public String getAffixWord() {
		return affixWord;
	}
	public void setAffixWord(String affixWord) {
		this.affixWord = affixWord;
	}
	public String getReplacementChar() {
		return replacementChar;
	}
	public void setReplacementChar(String replacementChar) {
		this.replacementChar = replacementChar;
	}
	public String getPosBefore() {
		return posBefore;
	}
	public void setPosBefore(String posBefore) {
		this.posBefore = posBefore;
	}
	public String getPosAfter() {
		return posAfter;
	}
	public void setPosAfter(String posAfter) {
		this.posAfter = posAfter;
	}
	
	public String toString() {
		return affixType + " " + affixWord + " " + replacementChar + " " + posBefore + " " + posAfter ;
	}
	/*public List<Rules> getChildRules() {
		return childRules;
	}
	public void setChildRules(List<Rules> childRules) {
		this.childRules = childRules;
	}*/
	
	
}
