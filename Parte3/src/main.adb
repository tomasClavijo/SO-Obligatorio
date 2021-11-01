with Ada.Text_IO; use Ada.Text_IO;

procedure main is

   task Patio is
      entry pedir;
      entry devolver;
   end Patio;
   task body Patio is
      ocupantes_patio : Integer := 0;
      i : Integer := 1;
      begin while i <= 10 loop
         select
            when ocupantes_patio < 2 =>
               accept pedir do
                  ocupantes_patio := ocupantes_patio + 1;
                  Put_Line("Ocupa en el valor:" & Integer'Image(i));
               end pedir;
         or
            accept devolver  do
               ocupantes_patio := ocupantes_patio - 1;
               Put_Line("Desocupa en el valor:" & Integer'Image(i));
            end devolver;
         end select;
         i := i + 1;
      end loop;
   end Patio;


   task Alice is
      entry Start;
   end Alice;
   task body Alice is
         begin loop
            Patio.pedir;
            Put_Line("Alice");
            Put_Line("pasea perro.");
            Patio.devolver;
         end loop;
   end Alice;




   task Bernardo is
      entry Start;
   end Bernardo;
   task body Bernardo is
         begin loop
            Patio.pedir;
            Put_Line("Bernardo");
            Put_Line("pasea perro.");
            Patio.devolver;
         end loop;
   end Bernardo;



   task Charlie is
      entry Start;
   end Charlie;
   task body Charlie is
         begin loop
            Patio.pedir;
            Put_Line("Charlie");
            Put_Line("pasea perro.");
            Patio.devolver;
         end loop;
   end Charlie;



   task Carla is
      entry Start;
   end Carla;
   task body Carla is
         begin loop
            Patio.pedir;
            Put_Line("Carla");
            Put_Line("pasea perro.");
            Patio.devolver;
         end loop;
   end Carla;

begin
   Alice.Start;
   Bernardo.Start;
   Charlie.Start;
   Carla.Start;

   Put_Line ("In main");
end;
--  procedure Show_Simple_Task is
--
--     task A;
--     task body A is
--     begin
--        Put_Line ("In task A");
--     end A;
--
--     task B;
--     task body B is
--     begin
--        Put_Line ("In task B");
--     end B;
--
--     task C;
--     task body C is
--     begin
--        Put_Line ("In task C");
--     end C;
--
--     begin
--        Put_Line ("In main");
--     end Show_Simple_Task;
