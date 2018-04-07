import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.io.File;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileNotFoundException;
import java.io.FileWriter;
import java.io.FileReader;
import java.io.IOException;

public class WaypointGenerator {
    public static void main(String[] args) throws FileNotFoundException {
        String begin = "QGC WPL 110\n";
        begin += "0\t1\t3\t112\t1\t0\t0\t0\t0\t0\t0\t1\n";
        begin += "1\t0\t3\t211\t1\t0\t0\t0\t0\t0\t1\n";
        begin += "2\t0\t3\t22\t0\t0\t0\t0\t0.0\t0.0\t20.0\t1\n";
        BufferedReader in = new BufferedReader(new FileReader("/Users/Guest/Downloads/SBHS-hackathon-master/src/Coordinates.txt"));
        ArrayList<float[]> coords = new ArrayList<float[]>();
        String line;
        try {
            while((line = in.readLine()) != null)
            {
                coords.add(processLine(line));
            }
            in.close();
            File file = new File("/Users/Guest/Downloads/SBHS-hackathon-master/src/Waypoints.txt");
            BufferedWriter writer = new BufferedWriter(new FileWriter("/Users/Guest/Downloads/SBHS-hackathon-master/src/Waypoints.txt"));
            writer.write(begin);
            int numLine = 3;                        //change this value if we add more to begin!
            for(float[] point : coords) {
                writer.write(processPoint(point, numLine));
                numLine++;
            }
            String end = numLine + "\t0\t3\t21\t0\t0\t0\t0\t" + coords.get(coords.size() - 1)[0] + "\t" + coords.get(coords.size() - 1)[1] + "\t0\t1\n";
            end += ++numLine + "\t0\t3\t211\t1\t0\t0\t0\t0\t0\t1";
            writer.write(end);
            writer.close();
            File waypoints = new File("/Users/Guest/Downloads/SBHS-hackathon-master/src/Waypoints.waypoints");
            file.renameTo(waypoints);
        } catch (IOException e) {
            System.out.println("Exception Occurred:");
            e.printStackTrace();
        }/*
        for(float[] f : coords) {
            System.out.println(f[0] + ", " + f[1]);
        }*/
    }

    public static float[] processLine(String s) {
        float[] ret = new float[2];
        int indexOfComma = s.indexOf(',');
        ret[0] = Float.valueOf(s.substring(0, indexOfComma));
        ret[1] = Float.valueOf(s.substring(indexOfComma + 1));
        return ret;
    }

    public static String processPoint(float[] coords, int lineLabel) {
        return lineLabel + "\t0\t3\t16\t0\t0\t0\t0\t" + coords[0] + "\t" + coords[1] + "\t7.0\t1\n";
    }
}
