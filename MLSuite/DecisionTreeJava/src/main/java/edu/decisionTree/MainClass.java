package edu.decisionTree;

/**
 * @author sagar
 *
 */
public class MainClass {
	public static void main(String[] args) {
		if (args == null || args.length == 0) {
			printError();
			System.exit(1);
		}

		MachineLearning machineLearning = new MachineLearning();
		if (args[0].trim().equalsIgnoreCase("predict")) {
			if(args.length != 3) {
				printError();
				System.exit(1);
			}
			machineLearning.predict(args[1].trim(),args[2].trim(),-1,false);
		} else if (args[0].trim().equalsIgnoreCase("evaluate")) {
			if(args.length != 2) {
				printError();
				System.exit(1);
			}
			machineLearning.evaluate(args[1].trim());
		}else if (args[0].trim().equalsIgnoreCase("predict-depth")) {
			if(args.length != 4) {
				printError();
				System.exit(1);
			}
			int maxDepth = -1;
			try {
				maxDepth = Integer.parseInt(args[3].trim());
			} catch(Exception e) {
				e.printStackTrace();
			}
			machineLearning.predict(args[1].trim(),args[2].trim(),maxDepth,false);
		}else if (args[0].trim().equalsIgnoreCase("evaluate-depth")) {
			if(args.length != 2) {
				printError();
				System.exit(1);
			}
			machineLearning.evaluateDepth(args[1].trim());
		}else if (args[0].trim().equalsIgnoreCase("predict-missing")) {
			if(args.length != 4) {
				printError();
				System.exit(1);
			}
			int treatment = 3;
			try {
				treatment = Integer.parseInt(args[3].trim());
			} catch(Exception e) {
				e.printStackTrace();
			}
			machineLearning.predict(args[1].trim(),args[2].trim(),treatment,true);
		}else if (args[0].trim().equalsIgnoreCase("evaluate-missing")) {
			if(args.length != 2) {
				printError();
				System.exit(1);
			}
			machineLearning.evaluateMissing(args[1].trim());
		} else {
			printError();
		}

	}
	
	private static void printError() {
		/*System.out.println(
				"This program needs at least 3 inputs - \n1. Desired function - predict/eveluate\n2.Path of the input file\n");*/
			System.out.println("ERROR IN INPUT! Please provide all the required inputs\n"+
					"If you want to train and test the model, first argument must be \"predict\" "
					+ ",second argument must be the absolute path of the training data file"
							+ " and third argument must be the absolute path of the test data file");
			System.out.println("If you want to train and test the model with a depth, first argument must be \"predict-depth\" "
					+ ",second argument must be the absolute path of the training data file"
					+ ",third argument must be the absolute path of the test data file"
							+ " and fourth argument must be the depth");
			System.out.println("If you want to train and test the model with a treatment for missing feature values, first argument must be \"predict-missing\" "
					+ ",second argument must be the absolute path of the training data file"
					+ ",third argument must be the absolute path of the test data file"
							+ " and fourth argument must be the value of treatment " + "\n"
							+ "(1 = Replace missing data with majority value of that feature)" + "\n"
							+ "(2 = Replace missing data with majority value of that feature against that label)" + "\n"
							+ "(3 = Don't replace missing values)");
		
			System.out.println("ERROR IN INPUT! Please provide all the required inputs\n"+
					"If you want to evaluate (cross validate) the model, first argument must be \"evaluate\" "
					+ "and second argument must be the absolute path of the cross validation data directory");
			System.out.println("If you want to evaluate (cross validate) the model with multiple depths, first argument must be \"evaluate-depth\" "
					+ "and second argument must be the absolute path of the cross validation data directory");
			System.out.println("If you want to evaluate (cross validate) the model a treatment for missing feature values, first argument must be \"evaluate-missing\" "
					+ "and second argument must be the absolute path of the cross validation data directory");
			System.out.println("\n Thank you ... Exiting");
	}
}
