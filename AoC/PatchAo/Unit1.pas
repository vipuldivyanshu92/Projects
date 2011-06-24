unit Unit1;

interface

uses
  Windows, Messages, SysUtils, Variants, Classes, Graphics, Controls, Forms,
  Dialogs, StdCtrls;

type
  TForm1 = class(TForm)
    Edit1: TEdit;
    Edit2: TEdit;
    Edit3: TEdit;
    Button1: TButton;
    Button2: TButton;
    Label1: TLabel;
    Label2: TLabel;
    Label3: TLabel;
    procedure Button1Click(Sender: TObject);
    procedure Button2Click(Sender: TObject);
  private
    { Déclarations privées }
  public
    { Déclarations publiques }
  end;

var
  Form1: TForm1;

implementation

{$R *.dfm}

function HexToInt (Value : string) : Integer; 
begin
    result := StrToInt('$'+Value);
end;

function GetHandle(name : PAnsiChar) : THandle;
var
    h_window : HWND;
    pid_process : DWORD;
    h_process : THandle;
begin
    // Looking for the window
    h_window := FindWindow(nil, name);
    if h_window = 0 then
        RaiseLastOSError;

    // Get the PID from the handle of the window
    GetWindowThreadProcessId(h_window, pid_process);

    // Getting a handle on the process with the PID
    h_process := OpenProcess(PROCESS_ALL_ACCESS, False, pid_process);
    if h_process = 0 then
        RaiseLastOSError;

    Result := h_process;
end;

    //    Memo1.Lines.Add('Success Getting process handle');
    //    //address := $008EF660;
    //    VirtualProtectEx(hProcess, Pointer($012B84C0), 256, PAGE_READWRITE, OldProtect);
    //    ReadProcessMemory(hProcess, Pointer($012B84C0), @damageBlockAddress, 256, bytesRead);
    //    //isequal := CompareMem(@damageBlockAddress, @DEFAULT_KEY[1], 256);
    //    //if isequal then
    //    //    Memo1.Lines.Add('Equal !');
    //    Memo1.Lines.Add(string(damageBlockAddress));
    //    //WriteProcessMemory(hProcess, Pointer($012B84C0), @value, 256, bytesWritten);
    //    CloseHandle(hProcess);
procedure TForm1.Button1Click(Sender: TObject);
var
    h_process : THandle;
    OldProtect : DWORD;
    FUNCOM_KEY : array [0..255] of char;
    bytesRead : DWORD;
    offset : DWORD;
begin
    h_process := GetHandle('Age of Conan');
    offset := HexToInt(Edit1.Text);
    VirtualProtectEx(h_process, Pointer(offset), 256, PAGE_READWRITE, OldProtect);
    ReadProcessMemory(h_process, Pointer(offset), @FUNCOM_KEY, 256, bytesRead);
    Edit2.Text := string(FUNCOM_KEY);
    CloseHandle(h_process);
end;

procedure TForm1.Button2Click(Sender: TObject);
var
    h_process : THandle;
    OldProtect : DWORD;
    PRIVATE_KEY : array [0..255] of char;
    bytesWritten : DWORD;
    offset : DWORD;
begin
    h_process := GetHandle('Age of Conan');
    offset := HexToInt(Edit1.Text);
    VirtualProtectEx(h_process, Pointer(offset), 256, PAGE_READWRITE, OldProtect);
    CopyMemory(@PRIVATE_KEY, @Edit3.Text[1], 256);
    WriteProcessMemory(h_process, Pointer(offset), @PRIVATE_KEY, 256, bytesWritten);
    CloseHandle(h_process);
end;

end.
