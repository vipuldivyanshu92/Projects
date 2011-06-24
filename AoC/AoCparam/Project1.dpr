program Project1;

{$APPTYPE CONSOLE}

uses
  SysUtils, ShellApi, Windows;

var
    i : byte;
    date : TDateTime;
begin
    try
        //Writeln(IntToStr(ParamCount));
        //for i := 0 to ParamCount do
        //    Writeln(ParamStr(i));
        //Readln;
        //ShellExecute(0, 'OPEN', 'F:\Age Of Conan\AgeOfConanOrg.exe', PChar(format('%s %s %s %s', [ParamStr(1), ParamStr(2), ParamStr(3), ParamStr(4)])), nil, SW_SHOWNORMAL);
        TDateTime :

    except
    on E:Exception do
        Writeln(E.Classname, ': ', E.Message);
    end;
end.
