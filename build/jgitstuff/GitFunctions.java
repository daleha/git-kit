package gitutil;
import org.eclipse.jgit.api.*;
import org.eclipse.jgit.api.LsRemoteCommand;
import org.eclipse.jgit.lib.BaseRepositoryBuilder;
import org.eclipse.jgit.lib.Repository;
import org.eclipse.jgit.lib.Ref;
import java.util.*;
import java.io.*;

//requires jgit and jsch

public class GitFunctions
{
	public static ArrayList<String[]> listRepo (String URL)
	{
		BaseRepositoryBuilder br = new BaseRepositoryBuilder();
		Repository r;
		Collection<Ref> c;
		ArrayList<String[]> ret= new ArrayList<String[]>();

			
		try
		{		
			br.setBare();
			br.setWorkTree(new File("."));
			r =br.build();

			LsRemoteCommand com =new LsRemoteCommand(r);	
			System.out.println("Using URL:"+URL);
			com.setRemote(URL);
			c= com.call();

			for (Iterator<Ref> i = c.iterator(); i.hasNext(); )
			{
				
				Ref curr=i.next();
				String sha = curr.getObjectId().toString();
				sha=sha.replace("AnyObjectId[","").replace("]","");
				String inf[] = {curr.getName(),sha};
				ret.add(inf);
				System.out.println(inf[0]+":"+inf[1]);
			}

		}catch (Exception e)
		{
			System.out.println("Exception:"+e.getMessage());
		}

		return ret;
	}
/*
 * i'm a test stub!
	public static void main (String[] args)
	{
		listRepo("foo");
	}
	*/

}
