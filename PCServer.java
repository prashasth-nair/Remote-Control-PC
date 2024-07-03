import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;


public class PCServer {
    public static void main(String[] args) {
        int portNumber = 54321; // Choose any available port for broadcasting
        try{
            while (true) {
                broadcastIpAddress(portNumber);
                Thread.sleep(2000);//2 seconds delay
            }
        }
        catch(Exception e){
            e.printStackTrace();
        }
        }
       
    
    public static void broadcastIpAddress(int portNumber) {
       try {
            DatagramSocket socket = new DatagramSocket();
            socket.setBroadcast(true);

            String message = getLocalIpAddress();
            byte[] sendData = message.getBytes();

            String subset = getSubnet(message);

            // Broadcast the message to all devices in the same network
            DatagramPacket packet = new DatagramPacket(sendData, sendData.length,
                    InetAddress.getByName(subset+".255"), portNumber);
            socket.send(packet);

            // System.out.println("PC Server broadcasted its IP address:"+ message);

            socket.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
    private static String getSubnet(String ipAddress) {
        // Find the last occurrence of '.' in the IP address
        int lastDotIndex = ipAddress.lastIndexOf('.');

        // Extract the substring from the beginning of the IP address to the last occurrence of '.'
        String subnet = ipAddress.substring(0, lastDotIndex);

        return subnet;
    }
    private static String getLocalIpAddress() throws Exception {
        // Get the local IP address of the PC
        return InetAddress.getLocalHost().getHostAddress();
    }
}
