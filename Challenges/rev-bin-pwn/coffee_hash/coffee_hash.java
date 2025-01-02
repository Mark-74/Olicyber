public class coffee_hash {
   static String hash = "630:624:622:612:609:624:623:610:624:624:567:631:638:639:658:593:546:605:607:585:648:636:635:704:702:687:687:682:629:699:633:639:634:637:578:622:620:617:606:615:568:633:589:587:645:639:653:654:633:634";

   public static void main(String... var0) {
      if (var0.length != 1) {
         System.out.println("Usage: java Challenge <password>");
         System.exit(1);
      }

      if (checkPassword(var0[0])) {
         System.out.printf("flag{%s}\n", var0[0]);
      } else {
         System.out.println("Incorrect password!");
      }

   }

   public static boolean checkPassword(String var0) {
      String var1 = "";

      for(int var2 = 0; var2 < var0.length(); ++var2) {
         int var3 = 0;

         for(int var4 = 0; var4 < 7; ++var4) {
            var3 += var0.charAt((var2 + var4) % var0.length());
         }

         var1 = var1 + (var1.length() == 0 ? var3 : ":" + var3);
      }

      return hash.equals(var1);
   }
}
