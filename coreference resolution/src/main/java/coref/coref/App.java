package coref.coref;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.Map;
import java.util.TreeMap;
import java.util.stream.Collectors;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;
import javax.xml.transform.OutputKeys;
import javax.xml.transform.Transformer;
import javax.xml.transform.TransformerConfigurationException;
import javax.xml.transform.TransformerException;
import javax.xml.transform.TransformerFactory;
import javax.xml.transform.TransformerFactoryConfigurationError;
import javax.xml.transform.dom.DOMSource;
import javax.xml.transform.stream.StreamResult;

import org.w3c.dom.Attr;
import org.w3c.dom.DOMException;
import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;
import org.xml.sax.SAXException;

/**
 * Hello world!
 *
 */
public class App 
{
	 public static void main( String[] args )
	    {
	    	try {
				Files.lines(Paths.get(args[0])).forEach(line -> doResolution(line, args[1]));;
			} catch (IOException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
	    }
	    
	    public static void doResolution(String inputFile, String outputDirectory){
	    	Map<Integer, String> anaphoraMap = new TreeMap<>();
	    	Map<String, String> antecedentMap = new TreeMap<>();
	        System.out.println( inputFile );
	        try {
//				String s = Files.lines(Paths.get(args[0])).map(line -> line.replaceAll("<[^>]+>", "")).collect(Collectors.joining("\n"));
	        	String s = Files.lines(Paths.get(inputFile)).map(line -> line).collect(Collectors.joining("\n"));
//				System.out.println(s);
				/*Properties props = new Properties();

				//props.setProperty("annotators","tokenize, cleanxml, ssplit, pos, lemma, parse, ner, depparse");
				props.setProperty("annotators","tokenize, cleanxml, ssplit, pos, lemma, parse, ner");

				StanfordCoreNLP pipeline = new StanfordCoreNLP(props);
				Annotation annotation = new Annotation(s);
				pipeline.annotate(annotation);
				List<CoreMap> sentences = annotation.get(CoreAnnotations.SentencesAnnotation.class);
				for (CoreMap sentence : sentences) {
				    for (CoreLabel token: sentence.get(CoreAnnotations.TokensAnnotation.class)) {
				        String word = token.get(CoreAnnotations.TextAnnotation.class);
				        // this is the POS tag of the token
				        String pos = token.get(CoreAnnotations.PartOfSpeechAnnotation.class);
				        System.out.print(word + "/" + pos +" \t ");

				        // this is the POS tag of the token
				        String dep = token.get(CoreAnnotations.PartOfSpeechAnnotation.class);
				        System.out.print(word + "/" + pos +" \t ");
				        
				        // this is the NER of the token
				        String ner = token.get(CoreAnnotations.NamedEntityTagAnnotation.class);
				        if(!("O").equals(ner))System.out.println(word + "/" + ner);
				        else System.out.println();
				        
				        }
				}
				*/
				//get anaphora
		        File fXmlFile = new File(inputFile);
		    	DocumentBuilderFactory dbFactory = DocumentBuilderFactory.newInstance();
		    	DocumentBuilder dBuilder = dbFactory.newDocumentBuilder();
		    	Document doc = dBuilder.parse(fXmlFile);
		    	Document out = dBuilder.newDocument();
		    	Element root = out.createElement("TXT");
		    	out.appendChild(root);

		    	//optional, but recommended
		    	//read this - http://stackoverflow.com/questions/13786607/normalization-in-dom-parsing-with-java-how-does-it-work
		    	doc.getDocumentElement().normalize();
		    	System.out.println(doc.getElementsByTagName("TXT"));
		    	NodeList nList = doc.getElementsByTagName("COREF");
		    	int j = 1;
		    	for (int temp = 0; temp < nList.getLength(); temp++) {

		    		Node nNode = nList.item(temp);
		    		int id = Integer.parseInt(nNode.getAttributes().getNamedItem("ID").getTextContent());
		    		String val = nNode.getTextContent();
		    		String ref = "";
		    		anaphoraMap.put(id, val);
	    			String sub = s.substring(0, s.indexOf("COREF ID=\"" + id + "\""));
		    		/*//exact pattern matching
		    		XPathFactory xFactory = XPathFactory.newInstance();
		            XPath xPath = xFactory.newXPath();
		            XPathExpression exp = xPath.compile("/TXT[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '" + nNode.getTextContent() + "')]");
		            
		            NodeList nl = (NodeList)exp.evaluate(doc.getFirstChild(), XPathConstants.NODESET);
		            for (int index = 0; index < nl.getLength(); index++) {

		                Node node = nl.item(index);
		                System.out.println("====\n" +node.getTextContent());

		            }
		    		*/
		    		boolean flag = false;
		    		for(Map.Entry<String, String> entry : antecedentMap.entrySet()){
		    			if(entry.getValue().equalsIgnoreCase(val)){
		    				ref = entry.getKey();
		    				flag = true;
		    				break;
		    			}
		    		}
		    		if(!flag){
			    		for(Map.Entry<Integer, String> entry : anaphoraMap.entrySet()){
			    			if(entry.getKey() < id && entry.getValue().equalsIgnoreCase(val)){
			    				ref = entry.getKey().toString();
			    				flag = true;
			    				break;
			    			}
			    		}
		    		}
		    		if(!flag && sub.toLowerCase().contains(val.toLowerCase())){
			    		/*String s1 = s.substring(0, sub.toLowerCase().indexOf(val.toLowerCase()));
			    		String s2 = s.substring(sub.toLowerCase().indexOf(val.toLowerCase()) + val.length());
			    		s = s1 + "<COREF ID=\"X" + j + "\">" + val + "</COREF" + s2;*/
			    		ref = "X" + j;

		    			Element antecedent = out.createElement("COREF");
		    			root.appendChild(antecedent);
		    			Attr attr = out.createAttribute("ID");
		    			attr.setValue(ref);
		    			antecedent.setAttributeNode(attr);
		    			
		    			antecedent.appendChild(out.createTextNode(val));
		    					
			    		System.out.println(sub.toLowerCase().contains(val.toLowerCase()) + " :: " + j);
			    		antecedentMap.put("X" + j++, val);
		    		}
		    		
			    		Attr refNode = doc.createAttribute("REF");
			    		refNode.setValue(ref);
			    		nNode.getAttributes().setNamedItem(refNode);
		
		    			Element ana = out.createElement("COREF");
		    			root.appendChild(ana);
		    			Attr attr = out.createAttribute("ID");
		    			attr.setValue(String.valueOf(id));
		    			ana.setAttributeNode(attr);
		    			
		    			refNode = out.createAttribute("REF");
			    		refNode.setValue(ref);
			    		ana.setAttributeNode(refNode);
		    			
		    			ana.setAttributeNode(refNode);
		    			
		    			ana.appendChild(out.createTextNode(val));
	    					
		    		
		    		System.out.println("\nCurrent Element :" + id + " :: " + val + " :: " + ref);
		    		

		    	}
		    	System.out.println(anaphoraMap);
		    	System.out.println(antecedentMap);
		    	Transformer transformer = TransformerFactory.newInstance().newTransformer();
		    	transformer.setOutputProperty(OutputKeys.INDENT, "no");

		    	//initialize StreamResult with File object to save to file
		    	StreamResult result = new StreamResult(new File("test.key"));
		    	DOMSource source = new DOMSource(doc);
		    	transformer.transform(source, result);

		    	transformer.setOutputProperty(OutputKeys.INDENT, "yes");
		    	String[] fileName = inputFile.split("/");;
		    	StreamResult res = new StreamResult(new File(outputDirectory, fileName[fileName.length -1].split("\\.")[0] + ".response"));
		    	DOMSource src = new DOMSource(out);
		    	transformer.transform(src, res);

			} catch (IOException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			} catch (ParserConfigurationException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			} catch (SAXException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			} catch (TransformerConfigurationException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			} catch (TransformerFactoryConfigurationError e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			} catch (TransformerException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			} catch (DOMException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
	    }
}
