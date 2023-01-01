using System;
//using System.Collections.Generic;
//using System.Linq;
//using System.Threading.Tasks;
using System.IO;
using System.Diagnostics;
using System.Security.Principal;
using System.Windows.Forms;

namespace windnd
{
    static class Program
    {
        /// <summary>
        /// The main entry point for the application.
        /// </summary>
        [STAThread]
        static void Main(string[] args)
        {
            //if (RunAsUser(args))
            //    return;
            Application.EnableVisualStyles();
            Application.SetCompatibleTextRenderingDefault(false);
            Application.Run(new Form1(args));
        }

     //   static string get_password_from_args(string userName, string[] args)
     //   {
     //       for(int i = 0; i < args.Length; i++)
     //       {
     //           if (args[i][0] == '-')
     //               continue;
     //           return args[i];
     //       }
     //       //return null;
     //       using (var pwf = new PWForm(userName))
     //       {
     //           var dr = pwf.ShowDialog();
     //           if (dr == DialogResult.OK)
     //           {
     //               return pwf.passwd;
     //           }
     //       }
     //       return null;
     //   }

     //   static bool RunAsUser(string[] args)
     //   {
     //       bool isElevated;
     //       using (WindowsIdentity identity = WindowsIdentity.GetCurrent())
     //       {
     //           WindowsPrincipal principal = new WindowsPrincipal(identity);
     //           isElevated = principal.IsInRole(WindowsBuiltInRole.Administrator);
     //       }
     //       if (!isElevated)
     //           return isElevated;

     //       // 첫번째 아규먼트를 암호로 설정!!! 아니면 암호를 물어봄
     //       string userName = System.Security.Principal.WindowsIdentity.GetCurrent().Name;
     //       string[] dom_user = userName.Split('\\');
     //       string passwd = get_password_from_args(dom_user[1], args);            

     //       string executable = System.Reflection.Assembly.GetEntryAssembly().Location;
     //       //string executable = "C:\\Windows\notepad.exe";
     //       ////string cwd = System.IO.Directory.GetCurrentDirectory();
     //       //string cwd = "C:\\work";
     //       ////ProcessStarter ps = new ProcessStarter(executable, cwd);
     //       ////ps.Run();
     //       //Impersonation.ExecuteAppAsLoggedOnUser("notepad", executable, cwd);

     //       // 프로세스 시작 정보 설정
     //       //MessageBox.Show("domain=<" + dom_user[0] + "> user=<" + dom_user[1] + ">");
     //       ProcessStartInfo startInfo = new ProcessStartInfo();
     //       startInfo.FileName = executable;
     //       // RunAs를 수행하기 위해 사용자 계정 정보를 초기화한다.
     //       startInfo.UserName = dom_user[1];
     //       startInfo.Password = new System.Security.SecureString();
     //       foreach (char ch in passwd)
     //       {
     //           startInfo.Password.AppendChar(ch);
     //       }
     //       startInfo.Domain = dom_user[0];
     //       // 사용자의 프로파일(HKEY_USERS 레지스트리 키)의 로드 여부 설정
     //       startInfo.LoadUserProfile = false;
     //       // 최대화 하여 시작하도록 설정
     //       // 이 값 역시 UseShellExecute가 false 이면 값을 명시적으로 주더라도 유효하지 않다. 즉, 무시된다.
     //       //startInfo.WindowStyle = ProcessWindowStyle.Maximized;
     //       // UserName, Password, Domain 속성이 설정되면 UseShellExecute는 false 이어야 한다.
     //       // UseShellExecute 속성이 false 이면 ErrorDialog 속성값은 무시된다.
     //       startInfo.UseShellExecute = false;
     //       try {
     //           // CreateProcessWithLogonW 를 통해 프로세스 구동
     //           Process p = Process.Start(startInfo);
     //           p.WaitForExit();
     //       }
     //       catch (Exception ex) {
     //           MessageBox.Show(ex.Message + "\r\n\r\n" + ex.StackTrace.ToString(),
     //               "Process.Start() Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
     //       }
     //    return isElevated;
     //}
    }
}
