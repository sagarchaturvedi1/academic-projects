package edu.nlp;

public class Output extends WordDictionary {
	
	private String source;

	public String getSource() {
		return source;
	}

	public void setSource(String source) {
		this.source = source;
	}
	
	@Override
	public String toString() {
		return word + " " + posTag + " ROOT=" + root + " SOURCE=" + source;
	}
}
