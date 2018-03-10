package es.eina;

import es.eina.analysis.sentiment.SentimentAnalysis;
import es.eina.loader.Loader;
import es.eina.parser.Parser;
import org.json.JSONArray;
import org.json.JSONObject;

import java.io.File;
import java.util.Arrays;

public class Main {

    private static File getFile(ClassLoader classLoader, String path){
        return new File(classLoader.getResource(path).getFile());
    }

    public static void main(String[] args) {

        parseDir();

        /*return;
        ClassLoader classLoader = Main.class.getClassLoader();
        File f = new File(classLoader.getResource("NBA-Data/TOR.json").getFile());
        JSONArray array = Loader.loadData(f);

        int neg = 0;
        int pos = 0;
        int zero = 0;

        SentimentAnalysis analysis = new SentimentAnalysis(getFile(classLoader, "lexicon.txt"));

        for(int i = 0 ; i < array.length(); i++){
            JSONObject obj = ((JSONObject) array.get(i));
            double points = analysis.analyse(obj.get("text").toString());

            if(points > 0.0){
                pos++;
            }else if(points < 0.0){
                neg++;
            }else{
                zero++;
            }

            System.out.println(obj.get("text") + " has " + points + " points.");
        }

        double total = pos + neg + zero;
        System.out.println("Pos: " + pos + " -> " + (pos / total) + " %.");
        System.out.println("Neg: " + neg + " -> " + (neg / total) + " %.");
        System.out.println("Zero: " + zero + " -> " + (zero / total) + " %.");
        System.out.println("Total: " + total);

        getAmount();*/
    }

    public static void getAmount() {
        int amount = 0;
        ClassLoader loader = Main.class.getClassLoader();
        File dir = getFile(loader, "NBA-Data");
        File[] files = dir.listFiles();
        for (File s : files){
            JSONArray array = Loader.loadData(s);
            amount += array.length();
        }

        System.out.println("Amount: " + amount);
    }

    public static void parseDir(){
        ClassLoader loader = Main.class.getClassLoader();
        SentimentAnalysis sentiment = new SentimentAnalysis(getFile(loader, "lexicon.txt"));
        File dir = getFile(loader, "NBA-Data");
        Parser.parseFiles(dir, new File("output"), sentiment);
    }

}
