#ifndef PYSIDE_DESTROY_LISTENER
#define PYSIDE_DESTROY_LISTENER


#include <QObject>
#include "pysidemacros.h"

namespace PySide
{
class DestroyListenerPrivate;
/// \deprecated This class is deprecated and isn't used by libpyside anymore.
class PYSIDE_API DestroyListener : public QObject
{
    Q_OBJECT
    public:
        PYSIDE_DEPRECATED(static DestroyListener* instance());
        static void destroy();
        void listen(QObject* obj);

    public slots:
        void onObjectDestroyed(QObject* obj);

    private:
        static DestroyListener* m_instance;
        DestroyListenerPrivate* m_d;
        DestroyListener(QObject *parent);
        ~DestroyListener();
};

}//namespace

#endif

