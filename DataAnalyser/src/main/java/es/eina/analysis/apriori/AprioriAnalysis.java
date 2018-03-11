package es.eina.analysis.apriori;

import weka.associations.Apriori;
import weka.core.Instances;
import weka.core.converters.ConverterUtils;
import weka.filters.Filter;
import weka.filters.unsupervised.attribute.NumericToNominal;

import java.io.File;

public class AprioriAnalysis {

    public static void analyze(){
        ConverterUtils.DataSource dataSource;
        try {
            dataSource = new ConverterUtils.DataSource("./output/CHI.csv");
        } catch (Exception e) {
            e.printStackTrace();
            return;
        }
        try {
            Instances data2 = dataSource.getDataSet();
            apriori(data2);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    private static void apriori(Instances data) throws Exception {
        // load data
        //data.setClassIndex(data.numAttributes() - 1);
        NumericToNominal filter = new NumericToNominal();
        filter.setOptions(new String[]{"-R", "1, 2, 3," + (data.numAttributes()-1)});
        filter.setInputFormat(data);

        Instances data2 = Filter.useFilter(data, filter);

        // build associator
        Apriori apriori = new Apriori();
        apriori.setClassIndex(data.classIndex());
        apriori.buildAssociations(data2);

        // output associator
        System.out.println(apriori);
    }

}
