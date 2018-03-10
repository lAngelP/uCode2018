package es.eina.analysis.sentiment;

import java.io.*;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

public class SentimentAnalysis {

    private Map<String, Double> positiveWords = new HashMap<>();
    private Map<String, Double> negativeWords = new HashMap<>();


    public SentimentAnalysis(File positiveFile){
        try {
            readFile(positiveFile);
        } catch (IOException e) {
            System.out.println("Cannot parse lexicon.");
        }
    }

    private void readFile(File f) throws IOException {
        BufferedReader reader = new BufferedReader(new FileReader(f));

        String line;

        while((line = reader.readLine()) != null){
            if(!line.startsWith("#")) {
                String[] split = line.split("\t", 6);
                if(split[0].isEmpty()){continue;}

                double posScore = Double.parseDouble(split[2]);
                double negScore = Double.parseDouble(split[3]);
                String[] word = split[4].split("#");
                for (String w: word) {
                    try{
                        Integer.parseInt(w);
                    }catch(NumberFormatException ex){
                        String parsedWord = w.toLowerCase().replace("[-_]", " ");
                        positiveWords.put(parsedWord, posScore);
                        negativeWords.put(parsedWord, negScore);
                    }
                }
            }

        }

    }

    public double analyse(String tweet){
        String[] data = tweet.split(" ");
        double value = 0;

        for (String str: data) {
            Double pos = positiveWords.get(str);
            Double neg = negativeWords.get(str);

            value += pos != null ? pos : 0.0;
            value -= neg != null ? neg : 0.0;
        }

        return value;
    }


}
